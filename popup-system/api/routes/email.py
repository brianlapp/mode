"""
Email ad endpoints: dynamic image ad and click redirect for ESPs.
Implements LiveIntent-style server-side rendering with deterministic rotation.
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response, RedirectResponse
from typing import Optional
from datetime import datetime
from database import get_db_connection
import sqlite3

import hashlib
import io
import json
import random

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

router = APIRouter()

VALID_PROPERTIES = ['mff', 'mmm', 'mcad', 'mmd']

def _resolve_property_code(raw: Optional[str]) -> str:
    if not raw:
        return 'mff'
    code = raw.strip().lower()
    return code if code in VALID_PROPERTIES else 'mff'

def _select_offer_for_send(property_code: str, send_id: str | None) -> dict | None:
    """Featured-first then RPM order; pick deterministic index based on send_id.

    If send_id is provided, use hash(send_id) to pick index; else default to first.
    """
    conn = get_db_connection()
    try:
        # Get featured campaign id (tolerate missing column on older DBs)
        featured_campaign_id = None
        try:
            cols_cur = conn.execute("PRAGMA table_info(properties)")
            prop_cols = [r[1] for r in cols_cur.fetchall()]
            if 'featured_campaign_id' in prop_cols:
                cur = conn.execute("SELECT featured_campaign_id FROM properties WHERE code = ?", (property_code,))
                row = cur.fetchone()
                featured_campaign_id = row[0] if row else None
        except sqlite3.Error:
            featured_campaign_id = None

        # Pull campaigns with RPM calculation
        cur = conn.execute(
            """
            SELECT 
                c.id,
                c.name,
                c.tune_url,
                c.logo_url,
                c.main_image_url,
                c.description,
                c.cta_text,
                c.offer_id,
                c.aff_id,
                -- RPM
                CASE 
                    WHEN COALESCE(impressions_count.total, 0) = 0 THEN 0
                    ELSE (COALESCE(revenue.total, 0) * 1000.0) / impressions_count.total
                END as rpm
            FROM campaigns c
            JOIN campaign_properties cp ON c.id = cp.campaign_id
            LEFT JOIN (
                SELECT campaign_id, COUNT(*) as total
                FROM impressions 
                WHERE property_code = ?
                GROUP BY campaign_id
            ) impressions_count ON c.id = impressions_count.campaign_id
            LEFT JOIN (
                SELECT campaign_id, SUM(revenue_estimate) as total
                FROM clicks 
                WHERE property_code = ?
                GROUP BY campaign_id
            ) revenue ON c.id = revenue.campaign_id
            WHERE c.active = 1 AND cp.active = 1 AND cp.property_code = ?
            ORDER BY 
                CASE WHEN ? IS NOT NULL AND c.id = ? THEN 0 ELSE 1 END,
                rpm DESC,
                c.created_at DESC
            """,
            (property_code, property_code, property_code, featured_campaign_id, featured_campaign_id)
        )
        campaigns = [dict(row) for row in cur.fetchall()]
        if not campaigns:
            return None

        if send_id:
            # Deterministic choice per send
            idx = int(hashlib.sha256(str(send_id).encode('utf-8')).hexdigest(), 16) % len(campaigns)
            return campaigns[idx]
        else:
            return campaigns[0]
    finally:
        conn.close()

def _draw_card_png(offer: dict, width: int, height: int) -> bytes:
    if not PIL_AVAILABLE:
        # If PIL not available, return 1x1 png
        return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\x1dc``\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"

    # Colors and fonts
    bg_color = (255, 255, 255, 255)
    border_color = (229, 231, 235, 255)  # gray-200
    title_color = (17, 24, 39, 255)      # gray-900
    text_color = (75, 85, 99, 255)       # gray-600
    cta_bg = (247, 0, 124, 255)          # Mode Pink
    cta_color = (255, 255, 255, 255)

    img = Image.new('RGBA', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Border + radius approximation
    draw.rounded_rectangle([(0, 0), (width - 1, height - 1)], radius=20, outline=border_color, width=2, fill=bg_color)

    # Load fonts (fallback to default if not available)
    try:
        title_font = ImageFont.truetype("arial.ttf", 28)
        body_font = ImageFont.truetype("arial.ttf", 16)
        cta_font = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        cta_font = ImageFont.load_default()

    padding = 24
    content_top = padding

    # Title
    title = offer.get('name') or offer.get('title') or 'Sponsored'
    draw.text((padding, content_top), title[:80], font=title_font, fill=title_color)
    content_top += 40

    # Image area: try to fetch and embed campaign image
    image_area_h = int(height * 0.45)
    image_rect = [padding, content_top, width - padding, content_top + image_area_h]
    draw.rounded_rectangle(image_rect, radius=12, fill=(243, 244, 246, 255))

    def _normalize_img_url(raw: str | None) -> str | None:
        if not raw:
            return None
        url = str(raw).strip()
        # Imgur links sometimes miss file extension; prefer i.imgur direct host
        if 'imgur.com/' in url and not url.startswith('https://i.imgur.com/'):
            parts = url.split('imgur.com/')
            tail = parts[1] if len(parts) > 1 else ''
            if '.' not in tail[-5:]:
                tail = tail.rstrip('/') + '.jpg'
            url = 'https://i.imgur.com/' + tail
        return url

    def _fetch_image_bytes(url: str) -> bytes | None:
        try:
            import requests
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry

            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (compatible; ModeEmailRenderer/1.0)'
            })
            retries = Retry(total=2, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504])
            adapter = HTTPAdapter(max_retries=retries)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            resp = session.get(url, timeout=5)
            if resp.status_code == 200 and resp.content:
                return resp.content
            return None
        except Exception:
            return None

    primary_url = _normalize_img_url(offer.get('main_image_url') or offer.get('image_url'))
    fallback_url = _normalize_img_url(offer.get('logo_url'))

    chosen_bytes = None
    if primary_url:
        chosen_bytes = _fetch_image_bytes(primary_url)
    if (chosen_bytes is None) and fallback_url:
        chosen_bytes = _fetch_image_bytes(fallback_url)

    if chosen_bytes is not None:
        from PIL import ImageOps
        try:
            ci = Image.open(io.BytesIO(chosen_bytes)).convert('RGB')
            # Fit into the image_rect with padding
            target_w = image_rect[2] - image_rect[0]
            target_h = image_rect[3] - image_rect[1]
            ci = ImageOps.contain(ci, (target_w, target_h))
            # Paste centered
            paste_x = image_rect[0] + (target_w - ci.width) // 2
            paste_y = image_rect[1] + (target_h - ci.height) // 2
            img.paste(ci, (paste_x, paste_y))
        except Exception:
            draw.text((padding + 10, content_top + 10), "img", font=body_font, fill=text_color)
    else:
        # Fallback placeholder
        draw.text((padding + 10, content_top + 10), "img", font=body_font, fill=text_color)
    content_top += image_area_h + 16

    # Description
    desc = offer.get('description') or ''
    if desc:
        draw.text((padding, content_top), desc[:120], font=body_font, fill=text_color)
        content_top += 28

    # CTA button
    cta_text = offer.get('cta_text') or 'View Offer'
    btn_h = 44
    btn_rect = [padding, height - padding - btn_h, width - padding, height - padding]
    draw.rounded_rectangle(btn_rect, radius=12, fill=cta_bg)
    # center text
    tw, th = draw.textlength(cta_text, font=cta_font), cta_font.size
    cx = (btn_rect[0] + btn_rect[2]) // 2
    cy = (btn_rect[1] + btn_rect[3]) // 2
    draw.text((cx - tw // 2, cy - th // 2), cta_text, font=cta_font, fill=cta_color)

    # Encode PNG
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

def _build_clickthrough_url(offer: dict, property_code: str, send: str | None, sub: str | None, esp: str | None) -> str:
    base = offer.get('tune_url') or ''
    # Append tracking params
    sep = '&' if ('?' in base) else '?'
    params = {
        'source': 'email',
        'subsource': esp or 'sendgrid',
        'utm_medium': 'email',
        'utm_source': esp or 'sendgrid',
        'utm_campaign': send or '',
        'property': property_code
    }
    qp = '&'.join([f"{k}={v}" for k, v in params.items() if v is not None])
    return f"{base}{sep}{qp}"

@router.get("/email/ad.png")
async def email_ad_png(request: Request, property: Optional[str] = None, send: Optional[str] = None, sub: Optional[str] = None, esp: Optional[str] = None, w: int = 600, h: int = 400):
    """Return a PNG ad card. Use unique query params to vary per send/sub.

    - property: mff|mmm|mcad (defaults to mff)
    - send: campaign/send identifier → deterministic rotation index
    - sub: subscriber id (optional; can be included just to make URL unique)
    - esp: sendgrid/clevertap/etc for attribution
    - w,h: size, default 600x400
    """
    try:
        prop = _resolve_property_code(property)
        offer = _select_offer_for_send(prop, send or sub)
        if not offer:
            raise HTTPException(status_code=404, detail="No active campaigns for property")

        # Track impression (server-side)
        try:
            conn = get_db_connection()
            conn.execute(
                """
                INSERT INTO impressions (
                    campaign_id, property_code, session_id, placement,
                    user_agent, timestamp, ip_hash, source, subsource, utm_campaign, referrer, landing_page
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    offer['id'],
                    prop,
                    sub or '',
                    'email',
                    (request.headers.get('user-agent') or '')[:255],
                    datetime.now().isoformat(),
                    hash(str(request.client.host)) if request.client else 0,
                    'email',
                    (esp or 'sendgrid')[:100],
                    (send or '')[:100],
                    (request.headers.get('referer') or '')[:255],
                    ''
                )
            )
            conn.commit()
            conn.close()
        except Exception:
            pass

        png_bytes = _draw_card_png(offer, max(200, min(w, 1200)), max(150, min(h, 800)))
        headers = {
            'Cache-Control': 'private, max-age=31536000',  # cache per distinct URL in ESP caches
            'Content-Type': 'image/png'
        }
        return Response(content=png_bytes, media_type='image/png', headers=headers)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to render email ad: {str(e)}")

@router.get("/email/click")
async def email_click_redirect(request: Request, property: Optional[str] = None, send: Optional[str] = None, sub: Optional[str] = None, esp: Optional[str] = None):
    """Log click and 302 to the campaign tracking link with email attribution."""
    try:
        prop = _resolve_property_code(property)
        offer = _select_offer_for_send(prop, send or sub)
        if not offer:
            raise HTTPException(status_code=404, detail="No active campaigns for property")

        # Log click
        try:
            conn = get_db_connection()
            conn.execute(
                """
                INSERT INTO clicks (
                    campaign_id, property_code, session_id, placement,
                    user_agent, timestamp, ip_hash, revenue_estimate,
                    source, subsource, utm_campaign, referrer, landing_page
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    offer['id'],
                    prop,
                    sub or '',
                    'email',
                    (request.headers.get('user-agent') or '')[:255],
                    datetime.now().isoformat(),
                    hash(str(request.client.host)) if request.client else 0,
                    0.45,
                    'email',
                    (esp or 'sendgrid')[:100],
                    (send or '')[:100],
                    (request.headers.get('referer') or '')[:255],
                    ''
                )
            )
            conn.commit()
            conn.close()
        except Exception:
            pass

        # Build redirect URL with attribution params
        redirect_url = _build_clickthrough_url(offer, prop, send, sub, esp)
        return RedirectResponse(url=redirect_url, status_code=302)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process click: {str(e)}")

"""
Email ad endpoints: dynamic image ad and click redirect for ESPs.
Implements LiveIntent-style server-side rendering with deterministic rotation.
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response, RedirectResponse
from typing import Optional
from datetime import datetime
from database import get_db_connection
import sqlite3

import hashlib
import io
import json
import random

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

router = APIRouter()

VALID_PROPERTIES = ['mff', 'mmm', 'mcad', 'mmd']

def _resolve_property_code(raw: Optional[str]) -> str:
    if not raw:
        return 'mff'
    code = raw.strip().lower()
    return code if code in VALID_PROPERTIES else 'mff'

def _select_offer_for_send(property_code: str, send_id: str | None) -> dict | None:
    """Featured-first then RPM order; pick deterministic index based on send_id.

    If send_id is provided, use hash(send_id) to pick index; else default to first.
    """
    conn = get_db_connection()
    try:
        # Get featured campaign id (tolerate missing column on older DBs)
        featured_campaign_id = None
        try:
            cols_cur = conn.execute("PRAGMA table_info(properties)")
            prop_cols = [r[1] for r in cols_cur.fetchall()]
            if 'featured_campaign_id' in prop_cols:
                cur = conn.execute("SELECT featured_campaign_id FROM properties WHERE code = ?", (property_code,))
                row = cur.fetchone()
                featured_campaign_id = row[0] if row else None
        except sqlite3.Error:
            featured_campaign_id = None

        # Pull campaigns with RPM calculation
        cur = conn.execute(
            """
            SELECT 
                c.id,
                c.name,
                c.tune_url,
                c.logo_url,
                c.main_image_url,
                c.description,
                c.cta_text,
                c.offer_id,
                c.aff_id,
                -- RPM
                CASE 
                    WHEN COALESCE(impressions_count.total, 0) = 0 THEN 0
                    ELSE (COALESCE(revenue.total, 0) * 1000.0) / impressions_count.total
                END as rpm
            FROM campaigns c
            JOIN campaign_properties cp ON c.id = cp.campaign_id
            LEFT JOIN (
                SELECT campaign_id, COUNT(*) as total
                FROM impressions 
                WHERE property_code = ?
                GROUP BY campaign_id
            ) impressions_count ON c.id = impressions_count.campaign_id
            LEFT JOIN (
                SELECT campaign_id, SUM(revenue_estimate) as total
                FROM clicks 
                WHERE property_code = ?
                GROUP BY campaign_id
            ) revenue ON c.id = revenue.campaign_id
            WHERE c.active = 1 AND cp.active = 1 AND cp.property_code = ?
            ORDER BY 
                CASE WHEN ? IS NOT NULL AND c.id = ? THEN 0 ELSE 1 END,
                rpm DESC,
                c.created_at DESC
            """,
            (property_code, property_code, property_code, featured_campaign_id, featured_campaign_id)
        )
        campaigns = [dict(row) for row in cur.fetchall()]
        if not campaigns:
            return None

        if send_id:
            # Deterministic choice per send
            idx = int(hashlib.sha256(str(send_id).encode('utf-8')).hexdigest(), 16) % len(campaigns)
            return campaigns[idx]
        else:
            return campaigns[0]
    finally:
        conn.close()

def _draw_card_png(offer: dict, width: int, height: int) -> bytes:
    if not PIL_AVAILABLE:
        # If PIL not available, return 1x1 png
        return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\x1dc``\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"

    # Colors and fonts
    bg_color = (255, 255, 255, 255)
    border_color = (229, 231, 235, 255)  # gray-200
    title_color = (17, 24, 39, 255)      # gray-900
    text_color = (75, 85, 99, 255)       # gray-600
    cta_bg = (247, 0, 124, 255)          # Mode Pink
    cta_color = (255, 255, 255, 255)

    img = Image.new('RGBA', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Border + radius approximation
    draw.rounded_rectangle([(0, 0), (width - 1, height - 1)], radius=20, outline=border_color, width=2, fill=bg_color)

    # Load fonts (fallback to default if not available)
    try:
        title_font = ImageFont.truetype("arial.ttf", 28)
        body_font = ImageFont.truetype("arial.ttf", 16)
        cta_font = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        cta_font = ImageFont.load_default()

    padding = 24
    content_top = padding

    # Title
    title = offer.get('name') or offer.get('title') or 'Sponsored'
    draw.text((padding, content_top), title[:80], font=title_font, fill=title_color)
    content_top += 40

    # Image area: try to fetch and embed campaign image
    image_area_h = int(height * 0.45)
    image_rect = [padding, content_top, width - padding, content_top + image_area_h]
    draw.rounded_rectangle(image_rect, radius=12, fill=(243, 244, 246, 255))
    def _normalize_img_url(raw: str | None) -> str | None:
        if not raw:
            return None
        url = str(raw).strip()
        # Imgur links sometimes miss file extension; prefer i.imgur direct host
        if 'imgur.com/' in url and not url.startswith('https://i.imgur.com/'):
            # Convert gallery/page links to direct image if possible
            parts = url.split('imgur.com/')
            tail = parts[1] if len(parts) > 1 else ''
            # If no extension, default to .jpg (Imgur serves correct type regardless)
            if '.' not in tail[-5:]:
                tail = tail.rstrip('/') + '.jpg'
            url = 'https://i.imgur.com/' + tail
        return url

    def _fetch_image_bytes(url: str) -> bytes | None:
        try:
            import requests
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry

            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (compatible; ModeEmailRenderer/1.0)'
            })
            retries = Retry(total=2, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504])
            adapter = HTTPAdapter(max_retries=retries)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            resp = session.get(url, timeout=5)
            if resp.status_code == 200 and resp.content:
                return resp.content
            return None
        except Exception:
            return None

    primary_url = _normalize_img_url(offer.get('main_image_url') or offer.get('image_url'))
    fallback_url = _normalize_img_url(offer.get('logo_url'))

    chosen_bytes = None
    if primary_url:
        chosen_bytes = _fetch_image_bytes(primary_url)
    if (chosen_bytes is None) and fallback_url:
        chosen_bytes = _fetch_image_bytes(fallback_url)

    if chosen_bytes is not None:
        from PIL import ImageOps
        try:
            ci = Image.open(io.BytesIO(chosen_bytes)).convert('RGB')
            # Fit into the image_rect with padding
            target_w = image_rect[2] - image_rect[0]
            target_h = image_rect[3] - image_rect[1]
            ci = ImageOps.contain(ci, (target_w, target_h))
            # Paste centered
            paste_x = image_rect[0] + (target_w - ci.width) // 2
            paste_y = image_rect[1] + (target_h - ci.height) // 2
            img.paste(ci, (paste_x, paste_y))
        except Exception:
            draw.text((padding + 10, content_top + 10), "img", font=body_font, fill=text_color)
    else:
        # Fallback placeholder
        draw.text((padding + 10, content_top + 10), "img", font=body_font, fill=text_color)
    else:
        # Fallback placeholder
        draw.text((padding + 10, content_top + 10), "img", font=body_font, fill=text_color)
    content_top += image_area_h + 16

    # Description
    desc = offer.get('description') or ''
    if desc:
        draw.text((padding, content_top), desc[:120], font=body_font, fill=text_color)
        content_top += 28

    # CTA button
    cta_text = offer.get('cta_text') or 'View Offer'
    btn_h = 44
    btn_rect = [padding, height - padding - btn_h, width - padding, height - padding]
    draw.rounded_rectangle(btn_rect, radius=12, fill=cta_bg)
    # center text
    tw, th = draw.textlength(cta_text, font=cta_font), cta_font.size
    cx = (btn_rect[0] + btn_rect[2]) // 2
    cy = (btn_rect[1] + btn_rect[3]) // 2
    draw.text((cx - tw // 2, cy - th // 2), cta_text, font=cta_font, fill=cta_color)

    # Encode PNG
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

def _build_clickthrough_url(offer: dict, property_code: str, send: str | None, sub: str | None, esp: str | None) -> str:
    base = offer.get('tune_url') or ''
    # Append tracking params
    sep = '&' if ('?' in base) else '?'
    params = {
        'source': 'email',
        'subsource': esp or 'sendgrid',
        'utm_medium': 'email',
        'utm_source': esp or 'sendgrid',
        'utm_campaign': send or '',
        'property': property_code
    }
    qp = '&'.join([f"{k}={v}" for k, v in params.items() if v is not None])
    return f"{base}{sep}{qp}"

@router.get("/email/ad.png")
async def email_ad_png(request: Request, property: Optional[str] = None, send: Optional[str] = None, sub: Optional[str] = None, esp: Optional[str] = None, w: int = 600, h: int = 400):
    """Return a PNG ad card. Use unique query params to vary per send/sub.

    - property: mff|mmm|mcad (defaults to mff)
    - send: campaign/send identifier → deterministic rotation index
    - sub: subscriber id (optional; can be included just to make URL unique)
    - esp: sendgrid/clevertap/etc for attribution
    - w,h: size, default 600x400
    """
    try:
        prop = _resolve_property_code(property)
        offer = _select_offer_for_send(prop, send or sub)
        if not offer:
            raise HTTPException(status_code=404, detail="No active campaigns for property")

        # Track impression (server-side)
        try:
            conn = get_db_connection()
            conn.execute(
                """
                INSERT INTO impressions (
                    campaign_id, property_code, session_id, placement,
                    user_agent, timestamp, ip_hash, source, subsource, utm_campaign, referrer, landing_page
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    offer['id'],
                    prop,
                    sub or '',
                    'email',
                    (request.headers.get('user-agent') or '')[:255],
                    datetime.now().isoformat(),
                    hash(str(request.client.host)) if request.client else 0,
                    'email',
                    (esp or 'sendgrid')[:100],
                    (send or '')[:100],
                    (request.headers.get('referer') or '')[:255],
                    ''
                )
            )
            conn.commit()
            conn.close()
        except Exception:
            pass

        png_bytes = _draw_card_png(offer, max(200, min(w, 1200)), max(150, min(h, 800)))
        headers = {
            'Cache-Control': 'private, max-age=31536000',  # cache per distinct URL in ESP caches
            'Content-Type': 'image/png'
        }
        return Response(content=png_bytes, media_type='image/png', headers=headers)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to render email ad: {str(e)}")

@router.get("/email/click")
async def email_click_redirect(request: Request, property: Optional[str] = None, send: Optional[str] = None, sub: Optional[str] = None, esp: Optional[str] = None):
    """Log click and 302 to the campaign tracking link with email attribution."""
    try:
        prop = _resolve_property_code(property)
        offer = _select_offer_for_send(prop, send or sub)
        if not offer:
            raise HTTPException(status_code=404, detail="No active campaigns for property")

        # Log click
        try:
            conn = get_db_connection()
            conn.execute(
                """
                INSERT INTO clicks (
                    campaign_id, property_code, session_id, placement,
                    user_agent, timestamp, ip_hash, revenue_estimate,
                    source, subsource, utm_campaign, referrer, landing_page
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    offer['id'],
                    prop,
                    sub or '',
                    'email',
                    (request.headers.get('user-agent') or '')[:255],
                    datetime.now().isoformat(),
                    hash(str(request.client.host)) if request.client else 0,
                    0.45,
                    'email',
                    (esp or 'sendgrid')[:100],
                    (send or '')[:100],
                    (request.headers.get('referer') or '')[:255],
                    ''
                )
            )
            conn.commit()
            conn.close()
        except Exception:
            pass

        # Build redirect URL with attribution params
        redirect_url = _build_clickthrough_url(offer, prop, send, sub, esp)
        return RedirectResponse(url=redirect_url, status_code=302)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process click: {str(e)}")


