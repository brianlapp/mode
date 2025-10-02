"""
Email Ad Management System
Comprehensive CRUD operations and serving endpoints for property-based email ads
"""

import os
import hashlib
import random
from pathlib import Path
from typing import Optional, Dict, Any, List
from io import BytesIO
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import logging
import datetime
import sqlite3
from database import get_db_connection

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic models for email ads
class EmailAdCreate(BaseModel):
    property_code: str
    name: str
    desktop_image_url: str
    mobile_image_url: Optional[str] = None
    click_url: str
    description: Optional[str] = None
    visibility_percentage: int = 100
    active: bool = True

class EmailAdUpdate(BaseModel):
    name: Optional[str] = None
    desktop_image_url: Optional[str] = None
    mobile_image_url: Optional[str] = None
    click_url: Optional[str] = None
    description: Optional[str] = None
    visibility_percentage: Optional[int] = None
    active: Optional[bool] = None

class EmailAdResponse(BaseModel):
    id: int
    property_code: str
    name: str
    desktop_image_url: str
    mobile_image_url: Optional[str]
    click_url: str
    description: Optional[str]
    visibility_percentage: int
    active: bool
    created_at: str
    updated_at: str

# ==============================================
# EMAIL AD SERVING ENDPOINTS (Primary API)
# ==============================================

def get_weighted_email_ad(property_code: str, variant: str = "desktop"):
    """Get email ad using visibility percentage rotation logic"""
    conn = get_db_connection()
    try:
        # Get all active email ads for property
        cursor = conn.execute("""
            SELECT id, name, desktop_image_url, mobile_image_url, click_url, visibility_percentage
            FROM email_ads
            WHERE property_code = ? AND active = 1
            ORDER BY id
        """, (property_code,))

        email_ads = cursor.fetchall()

        if not email_ads:
            return None

        # Apply visibility percentage weighting (same logic as campaigns)
        weighted_ads = []
        for ad in email_ads:
            weight = ad[5] if ad[5] > 0 else 1  # visibility_percentage
            weighted_ads.extend([ad] * weight)

        if not weighted_ads:
            return email_ads[0]  # Fallback to first ad

        # Random selection from weighted list
        selected_ad = random.choice(weighted_ads)

        return {
            'id': selected_ad[0],
            'name': selected_ad[1],
            'desktop_image_url': selected_ad[2],
            'mobile_image_url': selected_ad[3],
            'click_url': selected_ad[4],
            'visibility_percentage': selected_ad[5]
        }
    finally:
        conn.close()

def track_email_impression(email_ad_id: int, property_code: str, variant: str, recipient_hash: Optional[str] = None):
    """Track email ad impression"""
    conn = get_db_connection()
    try:
        conn.execute("""
            INSERT INTO email_ad_impressions (email_ad_id, property_code, variant, recipient_hash)
            VALUES (?, ?, ?, ?)
        """, (email_ad_id, property_code, variant, recipient_hash))
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to track impression: {e}")
    finally:
        conn.close()

def track_email_click(email_ad_id: int, property_code: str, variant: str, recipient_hash: Optional[str] = None):
    """Track email ad click"""
    conn = get_db_connection()
    try:
        conn.execute("""
            INSERT INTO email_ad_clicks (email_ad_id, property_code, variant, recipient_hash, revenue_estimate)
            VALUES (?, ?, ?, ?, ?)
        """, (email_ad_id, property_code, variant, recipient_hash, 0.25))  # Lower revenue than popup clicks
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to track click: {e}")
    finally:
        conn.close()

@router.get("/ad.png")
async def serve_email_ad(
    property: str = "mff",
    variant: str = "desktop",  # 'desktop' or 'mobile'
    recipient: str = None      # Optional recipient tracking
):
    """
    Serve rotating email ad for property
    - Gets active email ads for property
    - Applies visibility percentage rotation
    - Tracks impression
    - Returns redirect to selected ad image
    """
    try:
        # Get weighted email ad
        email_ad = get_weighted_email_ad(property.lower(), variant)

        if not email_ad:
            raise HTTPException(status_code=404, detail=f"No email ads found for property: {property}")

        # Track impression
        track_email_impression(
            email_ad['id'],
            property.lower(),
            variant,
            recipient
        )

        # Select image URL based on variant
        if variant == "mobile" and email_ad['mobile_image_url']:
            image_url = email_ad['mobile_image_url']
        else:
            image_url = email_ad['desktop_image_url']

        # Return redirect to image
        return RedirectResponse(url=image_url, status_code=302)

    except Exception as e:
        logger.error(f"Error serving email ad: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/click/{email_ad_id}")
async def track_email_click_endpoint(
    email_ad_id: int,
    property: str,
    variant: str = "desktop",
    recipient: str = None
):
    """
    Track email ad click and redirect to destination
    - Records click analytics
    - Returns redirect to click_url
    """
    try:
        # Get email ad
        conn = get_db_connection()
        cursor = conn.execute("""
            SELECT click_url FROM email_ads WHERE id = ? AND active = 1
        """, (email_ad_id,))

        email_ad = cursor.fetchone()
        conn.close()

        if not email_ad:
            raise HTTPException(status_code=404, detail="Email ad not found")

        # Track click
        track_email_click(email_ad_id, property.lower(), variant, recipient)

        # Redirect to destination
        return RedirectResponse(url=email_ad[0], status_code=302)

    except Exception as e:
        logger.error(f"Error tracking email click: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================
# EMAIL AD CRUD ENDPOINTS (Admin Management)
# ==============================================

@router.post("/", response_model=EmailAdResponse)
async def create_email_ad(email_ad: EmailAdCreate):
    """Create new email ad"""
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            INSERT INTO email_ads (
                property_code, name, desktop_image_url, mobile_image_url,
                click_url, description, visibility_percentage, active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            email_ad.property_code.lower(),
            email_ad.name,
            email_ad.desktop_image_url,
            email_ad.mobile_image_url,
            email_ad.click_url,
            email_ad.description,
            email_ad.visibility_percentage,
            email_ad.active
        ))

        email_ad_id = cursor.lastrowid
        conn.commit()

        # Return created email ad
        return await get_email_ad(email_ad_id)

    except Exception as e:
        logger.error(f"Error creating email ad: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.get("/", response_model=List[EmailAdResponse])
async def list_email_ads(property: str = None, active: bool = None):
    """List email ads with optional filters"""
    conn = get_db_connection()
    try:
        query = "SELECT * FROM email_ads"
        params = []
        conditions = []

        if property:
            conditions.append("property_code = ?")
            params.append(property.lower())

        if active is not None:
            conditions.append("active = ?")
            params.append(active)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY created_at DESC"

        cursor = conn.execute(query, params)
        email_ads = cursor.fetchall()

        return [
            EmailAdResponse(
                id=row[0],
                property_code=row[1],
                name=row[2],
                desktop_image_url=row[3],
                mobile_image_url=row[4],
                click_url=row[5],
                description=row[6],
                visibility_percentage=row[7],
                active=bool(row[8]),
                created_at=row[9],
                updated_at=row[10]
            ) for row in email_ads
        ]

    except Exception as e:
        logger.error(f"Error listing email ads: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.get("/{email_ad_id}", response_model=EmailAdResponse)
async def get_email_ad(email_ad_id: int):
    """Get email ad by ID"""
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT * FROM email_ads WHERE id = ?", (email_ad_id,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Email ad not found")

        return EmailAdResponse(
            id=row[0],
            property_code=row[1],
            name=row[2],
            desktop_image_url=row[3],
            mobile_image_url=row[4],
            click_url=row[5],
            description=row[6],
            visibility_percentage=row[7],
            active=bool(row[8]),
            created_at=row[9],
            updated_at=row[10]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting email ad: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.put("/{email_ad_id}", response_model=EmailAdResponse)
async def update_email_ad(email_ad_id: int, email_ad_update: EmailAdUpdate):
    """Update email ad"""
    conn = get_db_connection()
    try:
        # Build dynamic update query
        update_fields = []
        params = []

        for field, value in email_ad_update.model_dump(exclude_unset=True).items():
            if field == "property_code" and value:
                value = value.lower()
            update_fields.append(f"{field} = ?")
            params.append(value)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        params.append(email_ad_id)

        query = f"UPDATE email_ads SET {', '.join(update_fields)} WHERE id = ?"
        conn.execute(query, params)
        conn.commit()

        return await get_email_ad(email_ad_id)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating email ad: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.delete("/{email_ad_id}")
async def delete_email_ad(email_ad_id: int):
    """Delete email ad"""
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT id FROM email_ads WHERE id = ?", (email_ad_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Email ad not found")

        conn.execute("DELETE FROM email_ads WHERE id = ?", (email_ad_id,))
        conn.commit()

        return {"message": "Email ad deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting email ad: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# ==============================================
# EMAIL AD ANALYTICS ENDPOINTS
# ==============================================

@router.get("/analytics/summary")
async def get_email_analytics_summary(property: str = None):
    """Get email ad analytics summary"""
    conn = get_db_connection()
    try:
        # Base query for impressions
        impression_query = """
            SELECT ea.property_code, ea.name, COUNT(eai.id) as impressions
            FROM email_ads ea
            LEFT JOIN email_ad_impressions eai ON ea.id = eai.email_ad_id
        """

        # Base query for clicks
        click_query = """
            SELECT ea.property_code, ea.name, COUNT(eac.id) as clicks, SUM(eac.revenue_estimate) as revenue
            FROM email_ads ea
            LEFT JOIN email_ad_clicks eac ON ea.id = eac.email_ad_id
        """

        params = []
        if property:
            impression_query += " WHERE ea.property_code = ?"
            click_query += " WHERE ea.property_code = ?"
            params = [property.lower(), property.lower()]

        impression_query += " GROUP BY ea.id, ea.property_code, ea.name"
        click_query += " GROUP BY ea.id, ea.property_code, ea.name"

        # Get impressions
        impression_cursor = conn.execute(impression_query, params[:1] if params else [])
        impressions = {f"{row[0]}_{row[1]}": row[2] for row in impression_cursor.fetchall()}

        # Get clicks
        click_cursor = conn.execute(click_query, params[1:] if len(params) > 1 else params)
        clicks_data = {f"{row[0]}_{row[1]}": {"clicks": row[2], "revenue": row[3]} for row in click_cursor.fetchall()}

        # Combine data
        summary = []
        all_keys = set(impressions.keys()) | set(clicks_data.keys())

        for key in all_keys:
            prop, name = key.split("_", 1)
            impression_count = impressions.get(key, 0)
            click_data = clicks_data.get(key, {"clicks": 0, "revenue": 0})

            summary.append({
                "property_code": prop,
                "name": name,
                "impressions": impression_count,
                "clicks": click_data["clicks"],
                "ctr": round((click_data["clicks"] / impression_count * 100) if impression_count > 0 else 0, 2),
                "revenue": float(click_data["revenue"] or 0)
            })

        return {"summary": summary}

    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# ==============================================
# LEGACY COMPATIBILITY (for existing email.py calls)
# ==============================================

@router.get("/test")
async def test_email_ad_system():
    """Test endpoint to verify email ad system is working"""
    return {
        "message": "EMAIL AD MANAGEMENT SYSTEM IS ACTIVE!",
        "version": "3.0",
        "features": [
            "Email ad serving with rotation",
            "Click tracking",
            "CRUD operations",
            "Analytics",
            "Property-specific management"
        ],
        "timestamp": datetime.datetime.now().isoformat()
    }