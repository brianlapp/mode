"""
Property assignment API endpoints
Manage campaign visibility and settings per property (MFF, MMM, MCAD, MMD)
and resolve property by host for multi-domain support.
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Optional
from database import get_db_connection, detect_property_code_from_host
import sqlite3

router = APIRouter()

# Valid property codes
VALID_PROPERTIES = ['mff', 'mmm', 'mcad', 'mmd']

class PropertySetting(BaseModel):
    property_code: str
    visibility_percentage: int = 100  # 0-100%
    active: bool = True
    impression_cap_daily: Optional[int] = None
    click_cap_daily: Optional[int] = None

class PropertySettingUpdate(BaseModel):
    visibility_percentage: Optional[int] = None
    active: Optional[bool] = None
    impression_cap_daily: Optional[int] = None
    click_cap_daily: Optional[int] = None

@router.get("/campaigns/{campaign_id}/properties", response_model=List[PropertySetting])
async def get_campaign_property_settings(campaign_id: int):
    """Get property settings for a specific campaign"""
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            SELECT property_code, visibility_percentage, active,
                   impression_cap_daily, click_cap_daily
            FROM campaign_properties
            WHERE campaign_id = ?
            ORDER BY property_code
        """, (campaign_id,))
        
        settings = [dict(row) for row in cursor.fetchall()]
        return settings
    finally:
        conn.close()

@router.post("/campaigns/{campaign_id}/properties", response_model=dict)
async def set_campaign_property_settings(campaign_id: int, settings: List[PropertySetting]):
    """Set property settings for a campaign"""
    conn = get_db_connection()
    try:
        # Validate property codes
        for setting in settings:
            if setting.property_code not in VALID_PROPERTIES:
                raise HTTPException(status_code=400, detail=f"Invalid property code: {setting.property_code}")
            
            if not (0 <= setting.visibility_percentage <= 100):
                raise HTTPException(status_code=400, detail="Visibility percentage must be between 0 and 100")
        
        # Check if campaign exists
        cursor = conn.execute("SELECT id FROM campaigns WHERE id = ?", (campaign_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        # Delete existing settings for this campaign
        conn.execute("DELETE FROM campaign_properties WHERE campaign_id = ?", (campaign_id,))
        
        # Insert new settings
        for setting in settings:
            conn.execute("""
                INSERT INTO campaign_properties (
                    campaign_id, property_code, visibility_percentage, active,
                    impression_cap_daily, click_cap_daily
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                campaign_id,
                setting.property_code,
                setting.visibility_percentage,
                setting.active,
                setting.impression_cap_daily,
                setting.click_cap_daily
            ))
        
        conn.commit()
        return {"message": f"Property settings updated for campaign {campaign_id}"}
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@router.put("/campaigns/{campaign_id}/properties/{property_code}", response_model=dict)
async def update_property_setting(campaign_id: int, property_code: str, update: PropertySettingUpdate):
    """Update specific property setting for a campaign"""
    if property_code not in VALID_PROPERTIES:
        raise HTTPException(status_code=400, detail=f"Invalid property code: {property_code}")
    
    conn = get_db_connection()
    try:
        # Build dynamic update query
        update_fields = []
        values = []
        
        if update.visibility_percentage is not None:
            if not (0 <= update.visibility_percentage <= 100):
                raise HTTPException(status_code=400, detail="Visibility percentage must be between 0 and 100")
            update_fields.append("visibility_percentage = ?")
            values.append(update.visibility_percentage)
        
        if update.active is not None:
            update_fields.append("active = ?")
            values.append(update.active)

        if update.impression_cap_daily is not None:
            update_fields.append("impression_cap_daily = ?")
            values.append(update.impression_cap_daily)

        if update.click_cap_daily is not None:
            update_fields.append("click_cap_daily = ?")
            values.append(update.click_cap_daily)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        query = f"""
            UPDATE campaign_properties 
            SET {', '.join(update_fields)}
            WHERE campaign_id = ? AND property_code = ?
        """
        values.extend([campaign_id, property_code])
        
        cursor = conn.execute(query, values)
        
        if cursor.rowcount == 0:
            # Setting doesn't exist, create it
            conn.execute("""
                INSERT INTO campaign_properties (
                    campaign_id, property_code, visibility_percentage, active,
                    impression_cap_daily, click_cap_daily
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                campaign_id, 
                property_code, 
                update.visibility_percentage or 100,
                update.active if update.active is not None else True,
                update.impression_cap_daily,
                update.click_cap_daily
            ))
        
        conn.commit()
        return {"message": f"Property setting updated for {property_code}"}
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@router.get("/properties", response_model=List[str])
async def get_valid_properties():
    """Get list of valid property codes"""
    return VALID_PROPERTIES

@router.get("/properties/resolve", response_model=dict)
async def resolve_property(request: Request, host: Optional[str] = None):
    """Resolve property details by host header or explicit host param."""
    # Prefer explicit query param, else try forwarded/host headers
    hostname = (host or "").strip().lower()
    if not hostname:
        # Try common proxy headers
        forwarded = request.headers.get("x-forwarded-host") or request.headers.get("x-forwarded-server")
        header_host = request.headers.get("host")
        hostname = (forwarded or header_host or "").split(",")[0].strip().lower()
        # Strip port if present
        if ":" in hostname:
            hostname = hostname.split(":")[0]

    code = detect_property_code_from_host(hostname)

    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT code, name, domain, active, popup_enabled, popup_frequency, popup_placement FROM properties WHERE code = ?",
            (code,),
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"Property not found for host: {hostname}")

        return {
            "property_code": row[0],
            "name": row[1],
            "domain": row[2],
            "active": bool(row[3]),
            "popup_enabled": bool(row[4]),
            "popup_frequency": row[5],
            "popup_placement": row[6],
            "hostname": hostname,
        }
    finally:
        conn.close()

@router.put("/properties/{property_code}/featured")
async def set_featured_campaign(property_code: str, request: dict):
    """Set the featured campaign for a specific property"""
    try:
        campaign_id = request.get('campaign_id')
        
        # Validate property code
        if property_code not in VALID_PROPERTIES:
            raise HTTPException(status_code=400, detail=f"Invalid property code: {property_code}")
        
        conn = get_db_connection()
        
        # If campaign_id is provided, validate it exists
        if campaign_id:
            cursor = conn.execute("SELECT id FROM campaigns WHERE id = ? AND active = 1", (campaign_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Campaign not found or inactive")
        
        # Update the featured campaign for this property
        conn.execute("""
            UPDATE properties 
            SET featured_campaign_id = ? 
            WHERE code = ?
        """, (campaign_id, property_code))
        
        conn.commit()
        
        return {
            "success": True,
            "message": f"Featured campaign updated for {property_code}",
            "property_code": property_code,
            "featured_campaign_id": campaign_id
        }
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@router.get("/properties/{property_code}/featured")
async def get_featured_campaign(property_code: str):
    """Get the featured campaign for a specific property"""
    try:
        # Validate property code
        if property_code not in VALID_PROPERTIES:
            raise HTTPException(status_code=400, detail=f"Invalid property code: {property_code}")
        
        conn = get_db_connection()
        
        cursor = conn.execute("""
            SELECT p.featured_campaign_id, c.name as campaign_name
            FROM properties p
            LEFT JOIN campaigns c ON p.featured_campaign_id = c.id
            WHERE p.code = ?
        """, (property_code,))
        
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"Property not found: {property_code}")
        
        return {
            "property_code": property_code,
            "featured_campaign_id": row[0],
            "featured_campaign_name": row[1]
        }
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@router.get("/properties/{property_code}/campaigns", response_model=List[dict])
async def get_property_campaigns(property_code: str):
    """Get all campaigns configured for a specific property"""
    if property_code not in VALID_PROPERTIES:
        raise HTTPException(status_code=400, detail=f"Invalid property code: {property_code}")
    
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            SELECT 
                c.id,
                c.name,
                c.tune_url,
                c.logo_url,
                c.main_image_url,
                c.description,
                c.active as campaign_active,
                cp.visibility_percentage,
                cp.active as property_active
            FROM campaigns c
            JOIN campaign_properties cp ON c.id = cp.campaign_id
            WHERE cp.property_code = ?
            ORDER BY c.created_at DESC
        """, (property_code,))
        
        campaigns = [dict(row) for row in cursor.fetchall()]
        return campaigns
    finally:
        conn.close()

@router.delete("/campaigns/{campaign_id}/properties/{property_code}", response_model=dict)
async def remove_property_setting(campaign_id: int, property_code: str):
    """Remove property setting (deactivate campaign for specific property)"""
    if property_code not in VALID_PROPERTIES:
        raise HTTPException(status_code=400, detail=f"Invalid property code: {property_code}")
    
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            UPDATE campaign_properties 
            SET active = false
            WHERE campaign_id = ? AND property_code = ?
        """, (campaign_id, property_code))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Property setting not found")
        
        conn.commit()
        return {"message": f"Campaign deactivated for property {property_code}"}
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close() 