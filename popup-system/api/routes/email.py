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
from pathlib import Path
from urllib.parse import quote, unquote

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
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

def _select_offer_for_send(property_code: str, send_id: Optional[str]) -> Optional[dict]:
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

        # Pull campaigns with RPM calculation (prefer property-specific join)
        try:
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
        except sqlite3.Error:
            # Safety fallback if campaign_properties missing: use campaigns only
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
                    0 as rpm
                FROM campaigns c
                WHERE c.active = 1
                ORDER BY 
                    CASE WHEN ? IS NOT NULL AND c.id = ? THEN 0 ELSE 1 END,
                    c.created_at DESC
                """,
                (featured_campaign_id, featured_campaign_id)
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

def _draw_card_png(offer: dict, width: int, height: int, debug: bool = False, letter_spacing: Optional[float] = None) -> bytes:
    if not PIL_AVAILABLE:
        # If PIL not available, return 1x1 png
        return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\x1dc``\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"

    # Colors and fonts (match popup visual hierarchy)
    bg_color = (255, 255, 255, 255)
    border_color = (229, 231, 235, 255)  # light border
    title_color = (17, 24, 39, 255)      # gray-900
    text_color = (75, 85, 99, 255)       # gray-600
    cta_bg = (109, 40, 217, 255)         # MMM purple
    cta_color = (255, 255, 255, 255)

    img = Image.new('RGBA', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Border + radius approximation
    draw.rounded_rectangle([(0, 0), (width - 1, height - 1)], radius=20, outline=border_color, width=2, fill=bg_color)

    # Fixed-pixel rendering for 600x400 and 300x250
    if (width, height) in [(600, 400), (300, 250)]:
        # Helpers specific to fixed rendering path
        def _fonts_dir() -> Path:
            # Try multiple likely locations both locally and on Railway (Nixpacks)
            candidates = [
                Path(__file__).resolve().parents[3] / "assets" / "fonts",   # repo root /assets/fonts
                Path(__file__).resolve().parents[2] / "assets" / "fonts",   # popup-system/assets/fonts
                Path("/app/assets/fonts"),                                    # Railway image root
                Path("/workspace/assets/fonts"),                              # dev container
            ]
            for p in candidates:
                if p.exists():
                    return p
            # Fallback to repo root path even if not exists (will raise later)
            return candidates[0]

        def _ensure_inter_fonts(fonts_dir: Path) -> None:
            try:
                fonts_dir.mkdir(parents=True, exist_ok=True)
                title_path = fonts_dir / "Inter-ExtraBold.ttf"
                body_path = fonts_dir / "Inter-Regular.ttf"
                if not title_path.exists() or not body_path.exists():
                    import requests
                    urls = [
                        (title_path, "https://github.com/rsms/inter/raw/master/static/Inter-ExtraBold.ttf"),
                        (body_path, "https://github.com/rsms/inter/raw/master/static/Inter-Regular.ttf"),
                    ]
                    for path, url in urls:
                        if path.exists():
                            continue
                        try:
                            resp = requests.get(url, timeout=10)
                            if resp.status_code == 200 and resp.content:
                                with open(path, 'wb') as f:
                                    f.write(resp.content)
                        except Exception:
                            pass
            except Exception:
                pass

        def _load_inter(title_px: int, body_px: int, cta_px: int):
            try:
                ttf_title = str(_fonts_dir() / "Inter-ExtraBold.ttf")
                ttf_body = str(_fonts_dir() / "Inter-Regular.ttf")
                # Ensure fonts exist; download if missing (idempotent)
                _ensure_inter_fonts(Path(ttf_title).parent)
                return (
                    ImageFont.truetype(ttf_title, title_px),
                    ImageFont.truetype(ttf_body, body_px),
                    ImageFont.truetype(ttf_title, cta_px),
                )
            except Exception:
                try:
                    return (
                        ImageFont.truetype("DejaVuSans-Bold.ttf", title_px),
                        ImageFont.truetype("DejaVuSans.ttf", body_px),
                        ImageFont.truetype("DejaVuSans-Bold.ttf", cta_px),
                    )
                except Exception:
                    return (ImageFont.load_default(), ImageFont.load_default(), ImageFont.load_default())

        def _normalize_img_url(raw: Optional[str]) -> Optional[str]:
            if not raw:
                return None
            url = str(raw).strip()
            if 'imgur.com/' in url and not url.startswith('https://i.imgur.com/'):
                parts = url.split('imgur.com/')
                tail = parts[1] if len(parts) > 1 else ''
                if '.' not in tail[-5:]:
                    tail = tail.rstrip('/') + '.jpg'
                url = 'https://i.imgur.com/' + tail
            return url

        def _image_cache_dir() -> Path:
            candidates = [
                Path("/app/popup-system/api/cache"),
                Path("/app/api/cache"),
                Path(__file__).resolve().parents[3] / "cache",
            ]
            for p in candidates:
                try:
                    p.mkdir(parents=True, exist_ok=True)
                    return p
                except Exception:
                    continue
            return candidates[-1]

        def _internal_api_base() -> str:
            # Prefer public base to avoid self-call deadlocks; fallback to localhost for dev
            import os
            return os.environ.get("PUBLIC_BASE_URL") or "https://mode-dash-production.up.railway.app"

        def _proxied_url(u: str) -> str:
            # Route external images through our cached proxy to avoid rate limits
            try:
                return f"{_internal_api_base()}/api/proxy/img?u={quote(u, safe='')}"
            except Exception:
                return u

        def _fetch_image_bytes(url: Optional[str]) -> Optional[bytes]:
            if not url:
                return None
            try:
                import requests
                from requests.adapters import HTTPAdapter
                from urllib3.util.retry import Retry
                import hashlib, os

                session = requests.Session()
                session.headers.update({'User-Agent': 'Mozilla/5.0 (compatible; ModeEmailRenderer/1.0)'})
                retries = Retry(total=2, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504])
                adapter = HTTPAdapter(max_retries=retries)
                session.mount('http://', adapter)
                session.mount('https://', adapter)
                # Cache key
                h = hashlib.sha1(url.encode('utf-8')).hexdigest()
                cache_path = _image_cache_dir() / f"{h}.bin"
                if cache_path.exists():
                    try:
                        return cache_path.read_bytes()
                    except Exception:
                        pass
                # Try proxied first (shared cache and avoids 429s)
                try:
                    proxied = _proxied_url(url)
                    resp = session.get(proxied, timeout=8)
                    if resp.status_code == 200 and resp.content:
                        try:
                            cache_path.write_bytes(resp.content)
                        except Exception:
                            pass
                        return resp.content
                except Exception:
                    pass
                # Fallback to direct fetch
                resp = session.get(url, timeout=8)
                if resp.status_code == 200 and resp.content:
                    try:
                        cache_path.write_bytes(resp.content)
                    except Exception:
                        pass
                    return resp.content
            except Exception:
                return None
            return None

        def _draw_centered_with_tracking(text: str, y: int, font: ImageFont.FreeTypeFont, fill, tracking_px: float = 0.0):
            if not text:
                return
            total_w = 0.0
            for i, ch in enumerate(text):
                total_w += draw.textlength(ch, font=font)
                if i < len(text) - 1:
                    total_w += tracking_px
            x = int((width - total_w) // 2)
            cur_x = x
            for i, ch in enumerate(text):
                draw.text((cur_x, y), ch, font=font, fill=fill)
                cur_x += draw.textlength(ch, font=font)
                if i < len(text) - 1:
                    cur_x += tracking_px

        def _truncate_to_width(text: str, max_w: int, font: ImageFont.FreeTypeFont) -> str:
            t = (text or '').strip()
            if not t:
                return ''
            if draw.textlength(t, font=font) <= max_w:
                return t
            ell = '…'
            lo, hi = 0, len(t)
            best = ''
            while lo <= hi:
                mid = (lo + hi) // 2
                cand = t[:mid] + ell
                if draw.textlength(cand, font=font) <= max_w:
                    best = cand
                    lo = mid + 1
                else:
                    hi = mid - 1
            return best or ell

        # Size-specific numbers
        if (width, height) == (600, 400):
            badge_d = 56
            badge_x, badge_y = 24, 24
            title_px, body_px, cta_px = 44, 18, 22
            title_y = 92
            hero_rect = [24, 150, 576, 320]
            desc_y, desc_max_w = 330, 520
            cta_h, cta_side = 56, 60
            cta_top = height - 24 - cta_h
            track_px = (-0.5 if letter_spacing is None else float(letter_spacing))
        else:  # (300, 250)
            badge_d = 40
            badge_x, badge_y = 16, 16
            title_px, body_px, cta_px = 28, 12, 18
            title_y = 58
            # Derived from 600x400 spec with clean integers
            hero_rect = [12, 94, 288, 200]
            desc_y, desc_max_w = 206, 240
            cta_h, cta_side = 44, 28
            cta_top = height - 16 - cta_h
            track_px = (-0.25 if letter_spacing is None else float(letter_spacing))

        # Fonts
        title_font, body_font, cta_font = _load_inter(title_px, body_px, cta_px)

        # Badge/logo circle
        logo_url = _normalize_img_url(offer.get('logo_url'))
        if logo_url:
            try:
                content = _fetch_image_bytes(logo_url)
                if content:
                    badge_img = Image.open(io.BytesIO(content)).convert('RGB')
                    badge_img = ImageOps.fit(badge_img, (badge_d, badge_d), centering=(0.5, 0.5))
                    mask = Image.new('L', (badge_d, badge_d), 0)
                    mdraw = ImageDraw.Draw(mask)
                    mdraw.ellipse((0, 0, badge_d, badge_d), fill=255)
                    # white ring
                    ImageDraw.Draw(img).ellipse((badge_x - 2, badge_y - 2, badge_x + badge_d + 2, badge_y + badge_d + 2), fill=(255, 255, 255, 255))
                    img.paste(badge_img, (badge_x, badge_y), mask)
            except Exception:
                pass

        # Title (manual tracking)
        title_text = (offer.get('name') or offer.get('title') or 'Sponsored')[:80]
        _draw_centered_with_tracking(title_text, title_y, title_font, title_color, track_px)

        # Hero image (contain)
        def _fetch(url: Optional[str]):
            if not url:
                return None
            try:
                import requests
                r = requests.get(url, timeout=5)
                if r.status_code == 200 and r.content:
                    return r.content
            except Exception:
                return None
            return None
        primary = _normalize_img_url(offer.get('main_image_url') or offer.get('image_url'))
        fallback = _normalize_img_url(offer.get('logo_url'))
        img_bytes = _fetch_image_bytes(primary) or _fetch_image_bytes(fallback)
        if img_bytes:
            try:
                hi = Image.open(io.BytesIO(img_bytes)).convert('RGB')
                target_w = hero_rect[2] - hero_rect[0]
                target_h = hero_rect[3] - hero_rect[1]
                hi = ImageOps.contain(hi, (target_w, target_h), method=Image.BICUBIC)
                px = hero_rect[0] + (target_w - hi.width) // 2
                py = hero_rect[1] + (target_h - hi.height) // 2
                img.paste(hi, (px, py))
                # shadow ellipse
                ell_left = hero_rect[0] + int((target_w) * 0.1)
                ell_right = hero_rect[2] - int((target_w) * 0.1)
                ell_top = hero_rect[3] - 18
                ell_bottom = hero_rect[3] + 10
                shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
                ImageDraw.Draw(shadow).ellipse([ell_left, ell_top, ell_right, ell_bottom], fill=(0, 0, 0, 70))
                shadow = shadow.filter(ImageFilter.GaussianBlur(6))
                img_alpha = img if img.mode == 'RGBA' else img.convert('RGBA')
                img = Image.alpha_composite(img_alpha, shadow)
            except Exception:
                pass
        elif debug:
            # Draw placeholder box if image missing
            ImageDraw.Draw(img).rounded_rectangle(hero_rect, radius=10, outline=(209,213,219,255), width=2, fill=(243,244,246,255))
            ph = "IMG"
            lw = draw.textlength(ph, font=body_font)
            draw.text(((hero_rect[0]+hero_rect[2]-lw)//2, (hero_rect[1]+hero_rect[3]-body_px)//2), ph, font=body_font, fill=(156,163,175,255))

        # Description
        desc_text = (offer.get('description') or '').strip()
        if desc_text:
            line = _truncate_to_width(desc_text, desc_max_w, body_font)
            lw = draw.textlength(line, font=body_font)
            draw.text(((width - lw) // 2, desc_y), line, font=body_font, fill=text_color)

        # CTA button and safety rails
        btn = [cta_side, cta_top, width - cta_side, cta_top + cta_h]
        # Clamp to canvas
        btn[0] = max(0, btn[0])
        btn[1] = max(0, btn[1])
        btn[2] = min(width, btn[2])
        btn[3] = min(height, btn[3])
        draw.rounded_rectangle(btn, radius=12, fill=cta_bg)
        cta_text = offer.get('cta_text') or 'View Offer'
        tw = draw.textlength(cta_text, font=cta_font)
        tb = draw.textbbox((0, 0), cta_text, font=cta_font)
        th = (tb[3] - tb[1]) if tb else cta_font.size
        cx = (btn[0] + btn[2]) // 2
        cy = (btn[1] + btn[3]) // 2
        draw.text((int(cx - tw // 2), int(cy - th // 2)), cta_text, font=cta_font, fill=cta_color)

        # Debug guides
        if debug:
            # hero rect
            draw.rectangle(hero_rect, outline=(14, 165, 233, 200), width=1)
            # title baseline
            draw.line([(24, title_y), (width - 24, title_y)], fill=(14, 165, 233, 200), width=1)
            # desc max width box
            dl = (width - desc_max_w) // 2
            draw.rectangle([dl, desc_y - 2, dl + desc_max_w, desc_y + body_px + 2], outline=(14, 165, 233, 200), width=1)
            # cta rect outline
            draw.rectangle(btn, outline=(233, 84, 32, 200), width=1)

        # Encode and return early for fixed path
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()

    # Dynamic sizing based on canvas height to mirror popup proportions (legacy path)
    title_px = max(34, int(height * 0.12))
    body_px = max(16, int(height * 0.05))
    cta_px = max(18, int(height * 0.055))

    # Load fonts (fallback chain for production containers)
    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", title_px)
        body_font = ImageFont.truetype("DejaVuSans.ttf", body_px)
        cta_font = ImageFont.truetype("DejaVuSans-Bold.ttf", cta_px)
    except Exception:
        try:
            title_font = ImageFont.truetype("arial.ttf", title_px)
            body_font = ImageFont.truetype("arial.ttf", body_px)
            cta_font = ImageFont.truetype("arial.ttf", cta_px)
        except Exception:
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
            cta_font = ImageFont.load_default()

    padding = 24
    content_top = padding

    # Helper functions (declare before any use)
    def _normalize_img_url(raw: Optional[str]) -> Optional[str]:
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

    def _internal_api_base() -> str:
        import os
        return os.environ.get("PUBLIC_BASE_URL") or "https://mode-dash-production.up.railway.app"

    def _proxied_url(u: str) -> str:
        try:
            return f"{_internal_api_base()}/api/proxy/img?u={quote(u, safe='')}"
        except Exception:
            return u

    def _fetch_image_bytes(url: str) -> Optional[bytes]:
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
            # Try proxied fetch first
            try:
                proxied = _proxied_url(url)
                resp = session.get(proxied, timeout=6)
                if resp.status_code == 200 and resp.content:
                    return resp.content
            except Exception:
                pass
            # Fallback to direct fetch
            resp = session.get(url, timeout=6)
            if resp.status_code == 200 and resp.content:
                return resp.content
            return None
        except Exception:
            return None

    # Brand circle logo (top-left) like popup
    badge_d = 56
    logo_url_for_badge = offer.get('logo_url')
    if logo_url_for_badge:
        lb = _fetch_image_bytes(_normalize_img_url(logo_url_for_badge) or logo_url_for_badge)
        if lb:
            try:
                badge = Image.open(io.BytesIO(lb)).convert('RGB')
                badge = ImageOps.fit(badge, (badge_d, badge_d), centering=(0.5, 0.5))
                # Create circular mask
                mask = Image.new('L', (badge_d, badge_d), 0)
                mdraw = ImageDraw.Draw(mask)
                mdraw.ellipse((0, 0, badge_d, badge_d), fill=255)
                # Subtle white ring
                ring_rect = (padding - 2, padding - 2, padding - 2 + badge_d + 4, padding - 2 + badge_d + 4)
                ImageDraw.Draw(img).ellipse(ring_rect, fill=(255, 255, 255, 255))
                # Paste circle
                img.paste(badge, (padding, padding), mask)
            except Exception:
                pass

    # Title (centered, larger like popup)
    title = offer.get('name') or offer.get('title') or 'Sponsored'
    tw = draw.textlength(title[:80], font=title_font)
    draw.text(((width - tw) // 2, content_top + 2), title[:80], font=title_font, fill=title_color)
    content_top += int(title_px * 1.4)

    # Image area: hero style within padding (no distortion, no crop)
    image_area_h = int(height * 0.50)
    image_rect = [padding, content_top, width - padding, content_top + image_area_h]

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
            target_w = image_rect[2] - image_rect[0]
            target_h = image_rect[3] - image_rect[1]
            # Preserve aspect (no crop), center with padding
            ci = ImageOps.contain(ci, (target_w, target_h), method=Image.BICUBIC)
            paste_x = image_rect[0] + (target_w - ci.width) // 2
            paste_y = image_rect[1] + (target_h - ci.height) // 2
            img.paste(ci, (paste_x, paste_y))
            # Soft drop shadow ellipse underneath hero, like popup
            shadow_margin = int(target_w * 0.1)
            ell_rect = [image_rect[0] + shadow_margin, image_rect[3] - 18, image_rect[2] - shadow_margin, image_rect[3] + 10]
            shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
            ImageDraw.Draw(shadow).ellipse(ell_rect, fill=(0, 0, 0, 70))
            shadow = shadow.filter(ImageFilter.GaussianBlur(6))
            img = Image.alpha_composite(img, shadow)
        except Exception:
            draw.text((padding + 10, content_top + 10), "img", font=body_font, fill=text_color)
    else:
        # Fallback placeholder
        draw.text((padding + 10, content_top + 10), "img", font=body_font, fill=text_color)
    content_top += image_area_h + 16

    # Description (centered)
    desc = (offer.get('description') or '').strip()
    if desc:
        line = desc[:120]
        lw = draw.textlength(line, font=body_font)
        draw.text(((width - lw) // 2, content_top), line, font=body_font, fill=text_color)
        content_top += int(body_px * 1.6)

    # CTA button
    cta_text = offer.get('cta_text') or 'View Offer'
    btn_h = max(44, int(height * 0.13))
    side = max(40, int(width * 0.08))
    btn_rect = [padding + side, height - padding - btn_h, width - padding - side, height - padding]
    # Safety: ensure CTA stays on canvas in proportional path too
    if btn_rect[3] > height:
        delta = btn_rect[3] - height
        btn_rect[1] -= delta
        btn_rect[3] -= delta
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

def _build_clickthrough_url(offer: dict, property_code: str, send: Optional[str], sub: Optional[str], esp: Optional[str]) -> str:
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
async def email_ad_png(request: Request, property: Optional[str] = None, send: Optional[str] = None, sub: Optional[str] = None, esp: Optional[str] = None, w: int = 600, h: int = 400, debug: int = 0, ls: Optional[float] = None):
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

        # Enforce exact sizes when requesting 600x400 or 300x250 for visual parity
        target_w = 600 if (w == 600 and h == 400) else 300 if (w == 300 and h == 250) else max(200, min(w, 1200))
        target_h = 400 if (w == 600 and h == 400) else 250 if (w == 300 and h == 250) else max(150, min(h, 800))
        png_bytes = _draw_card_png(offer, target_w, target_h, debug=bool(debug), letter_spacing=ls)
        headers = {
            'Cache-Control': 'private, max-age=31536000',  # cache per distinct URL in ESP caches
            'Content-Type': 'image/png'
        }
        return Response(content=png_bytes, media_type='image/png', headers=headers)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to render email ad: {str(e)}")

@router.get("/email/ad.debug")
async def email_ad_debug(property: Optional[str] = None, send: Optional[str] = None, sub: Optional[str] = None, w: int = 600, h: int = 400):
    """Return JSON diagnostics for the email PNG renderer (no image).

    Includes: size path, selected campaign, font file presence, image URL checks.
    """
    try:
        prop = _resolve_property_code(property)
        offer = _select_offer_for_send(prop, send or sub)
        if not offer:
            raise HTTPException(status_code=404, detail="No active campaigns for property")

        # Enforce exact sizes for our fixed spec
        target_w = 600 if (w == 600 and h == 400) else 300 if (w == 300 and h == 250) else w
        target_h = 400 if (w == 600 and h == 400) else 250 if (w == 300 and h == 250) else h
        fixed = (target_w, target_h) in [(600, 400), (300, 250)]

        # Font presence
        def _fonts_dir() -> Path:
            candidates = [
                Path(__file__).resolve().parents[3] / "assets" / "fonts",
                Path(__file__).resolve().parents[2] / "assets" / "fonts",
                Path("/app/assets/fonts"),
                Path("/workspace/assets/fonts"),
            ]
            for p in candidates:
                if p.exists():
                    return p
            return candidates[0]

        fdir = _fonts_dir()
        ttf_title = fdir / "Inter-ExtraBold.ttf"
        ttf_body = fdir / "Inter-Regular.ttf"

        # URL normalization and fetch checks
        def _normalize(u: Optional[str]) -> Optional[str]:
            if not u:
                return None
            url = str(u).strip()
            if 'imgur.com/' in url and not url.startswith('https://i.imgur.com/'):
                parts = url.split('imgur.com/')
                tail = parts[1] if len(parts) > 1 else ''
                if '.' not in tail[-5:]:
                    tail = tail.rstrip('/') + '.jpg'
                url = 'https://i.imgur.com/' + tail
            return url

        def _check(url: Optional[str]):
            if not url:
                return {"url": None, "ok": False, "status": None, "error": "empty"}
            try:
                import requests
                r = requests.get(url, timeout=6)
                return {"url": url, "ok": (r.status_code == 200 and bool(r.content)), "status": r.status_code, "len": len(r.content) if r.content else 0}
            except Exception as e:
                return {"url": url, "ok": False, "status": None, "error": str(e)}

        primary = _normalize(offer.get('main_image_url') or offer.get('image_url'))
        fallback = _normalize(offer.get('logo_url'))
        primary_chk = _check(primary)
        fallback_chk = _check(fallback)

        return {
            "size": {"requested": [w, h], "actual": [target_w, target_h], "fixed_layout": fixed},
            "campaign": {"id": offer.get('id'), "name": offer.get('name') or offer.get('title'), "logo_url": offer.get('logo_url'), "main_image_url": offer.get('main_image_url') or offer.get('image_url')},
            "fonts": {"dir": str(fdir), "inter_extrabold_exists": ttf_title.exists(), "inter_regular_exists": ttf_body.exists()},
            "images": {"primary": primary_chk, "fallback": fallback_chk}
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Debug failed: {str(e)}")

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

@router.get("/proxy/img")
async def proxy_img(u: str):
    """Simple cached image proxy to avoid third-party rate limits.
    Query: u (encoded URL)
    """
    try:
        raw = unquote(u)
        if not raw.startswith("http"):
            raise HTTPException(status_code=400, detail="invalid url")
        # Cache path
        h = hashlib.sha1(raw.encode("utf-8")).hexdigest()
        cache_dir = Path("/app/popup-system/api/cache")
        try:
            cache_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
        cache_path = cache_dir / f"{h}.bin"
        if cache_path.exists():
            data = cache_path.read_bytes()
            return Response(content=data, media_type="image/jpeg")
        # Fetch with UA + retries
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (compatible; ModeImageProxy/1.0)'})
        retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        resp = session.get(raw, timeout=8)
        if resp.status_code == 200 and resp.content:
            try:
                cache_path.write_bytes(resp.content)
            except Exception:
                pass
            # Heuristic content type
            ctype = resp.headers.get('Content-Type') or 'image/jpeg'
            return Response(content=resp.content, media_type=ctype)
        raise HTTPException(status_code=resp.status_code, detail=f"fetch failed: {resp.status_code}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"proxy error: {str(e)}")

