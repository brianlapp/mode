"""
Campaign management API endpoints
CRUD operations for Mike's Tune campaign management
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from database import (
    get_db_connection, 
    insert_campaign, 
    get_active_campaigns_for_property,
    track_impression
)
import sqlite3
from datetime import datetime

router = APIRouter()

# Pydantic models for request/response
class CampaignCreate(BaseModel):
    name: str
    tune_url: str
    logo_url: str          # For top-left circle
    main_image_url: str    # For main offer display
    description: Optional[str] = ""
    cta_text: str = 'View Offer'
    offer_id: Optional[str] = ""  # Tune offer ID for impression pixels
    aff_id: Optional[str] = ""    # Tune affiliate ID for impression pixels

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    tune_url: Optional[str] = None
    logo_url: Optional[str] = None
    main_image_url: Optional[str] = None
    description: Optional[str] = None
    cta_text: Optional[str] = None
    active: Optional[bool] = None

class Campaign(BaseModel):
    id: int
    name: str
    tune_url: str
    logo_url: str
    main_image_url: str
    description: str
    cta_text: str
    offer_id: Optional[str] = ""
    aff_id: Optional[str] = ""
    active: bool
    created_at: str
    updated_at: str

class CampaignForPopup(BaseModel):
    id: int
    name: str
    tune_url: str
    logo_url: str
    main_image_url: str
    description: str
    visibility_percentage: int

@router.get("/campaigns", response_model=List[Campaign])
async def get_all_campaigns():
    """Get all campaigns for admin dashboard"""
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            SELECT * FROM campaigns 
            ORDER BY created_at DESC
        """)
        campaigns = [dict(row) for row in cursor.fetchall()]
        return campaigns
    finally:
        conn.close()

@router.get("/campaigns/{property_code}")
async def get_campaigns_for_property(property_code: str):
    """Get active campaigns for specific property (for popup script)"""
    if property_code not in ['mff', 'mmm', 'mcad', 'mmd']:
        raise HTTPException(status_code=400, detail="Invalid property code")
    
    # SIMPLE: Just return all campaigns for now to get popup working
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT * FROM campaigns WHERE active = 1 ORDER BY created_at DESC")
        campaigns = [dict(row) for row in cursor.fetchall()]
        return campaigns
    finally:
        conn.close()

@router.post("/campaigns", response_model=dict)
async def create_campaign(campaign: CampaignCreate):
    """Create new campaign"""
    try:
        campaign_id = insert_campaign(
            name=campaign.name,
            tune_url=campaign.tune_url,
            logo_url=campaign.logo_url,
            main_image_url=campaign.main_image_url,
            description=campaign.description,
            cta_text=campaign.cta_text,
            offer_id=campaign.offer_id,
            aff_id=campaign.aff_id
        )
        return {"id": campaign_id, "message": "Campaign created successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/campaigns/{campaign_id}", response_model=dict)
async def update_campaign(campaign_id: int, updates: CampaignUpdate):
    """Update existing campaign"""
    conn = get_db_connection()
    try:
        # Build dynamic update query
        update_fields = []
        values = []
        
        for field, value in updates.dict(exclude_unset=True).items():
            if value is not None:
                update_fields.append(f"{field} = ?")
                values.append(value)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        # Add updated_at timestamp
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        
        query = f"""
            UPDATE campaigns 
            SET {', '.join(update_fields)}
            WHERE id = ?
        """
        values.append(campaign_id)
        
        cursor = conn.execute(query, values)
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        conn.commit()
        return {"message": "Campaign updated successfully"}
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@router.delete("/campaigns/{campaign_id}", response_model=dict)
async def delete_campaign(campaign_id: int):
    """Delete campaign (sets active=false instead of actual deletion)"""
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            UPDATE campaigns 
            SET active = false, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (campaign_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        conn.commit()
        return {"message": "Campaign deactivated successfully"}
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@router.delete("/campaigns/{campaign_id}/hard-delete", response_model=dict)
async def hard_delete_campaign(campaign_id: int):
    """Permanently delete campaign from database"""
    conn = get_db_connection()
    try:
        # Delete from campaign_properties first (foreign key constraint)
        conn.execute("DELETE FROM campaign_properties WHERE campaign_id = ?", (campaign_id,))
        
        # Delete the campaign
        cursor = conn.execute("DELETE FROM campaigns WHERE id = ?", (campaign_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        conn.commit()
        return {"message": "Campaign permanently deleted"}
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@router.get("/campaigns/active/{property_code}")
async def get_active_campaigns_for_property(property_code: str):
    """Get active campaigns for a specific property (e.g., 'mff', 'mmm', 'mcad', 'mmd')"""
    try:
        conn = get_db_connection()
        cursor = conn.execute("""
            SELECT c.id, c.name, c.tune_url, c.logo_url, c.main_image_url, 
                   c.description, c.cta_text, c.offer_id, c.aff_id
            FROM campaigns c
            WHERE c.active = 1
            ORDER BY c.created_at DESC
        """)
        
        campaigns = []
        for row in cursor.fetchall():
            campaigns.append({
                "id": row[0],
                "name": row[1],
                "tune_url": row[2],
                "logo_url": row[3],
                "main_image_url": row[4],
                "description": row[5],
                "cta_text": row[6] or "View Offer",
                "offer_id": row[7],
                "aff_id": row[8]
            })
        
        conn.close()
        
        return {
            "success": True,
            "property_code": property_code,
            "campaigns": campaigns,
            "count": len(campaigns)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch campaigns: {str(e)}")


@router.post("/impression")
async def track_impression(request: Request):
    """Track popup impression event"""
    try:
        data = await request.json()
        
        # Basic validation
        required_fields = ["campaign_id", "property_code"]
        for field in required_fields:
            if field not in data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        conn = get_db_connection()
        
        # Insert impression record with Phase 2 tracking
        conn.execute("""
            INSERT INTO impressions (
                campaign_id, property_code, session_id, placement, 
                user_agent, timestamp, ip_hash, source, subsource, 
                utm_campaign, referrer, landing_page
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["campaign_id"],
            data["property_code"],
            data.get("session_id", ""),
            data.get("placement", "thankyou"),
            data.get("user_agent", "")[:255],  # Limit user agent length
            data.get("timestamp", datetime.now().isoformat()),
            hash(str(request.client.host)) if request.client else 0,  # Simple IP hash
            data.get("source", "")[:100],      # Phase 2: Traffic source
            data.get("subsource", "")[:100],   # Phase 2: Traffic subsource
            data.get("utm_campaign", "")[:100], # Phase 2: Campaign parameter
            data.get("referrer", "")[:255],    # Phase 2: Referrer URL
            data.get("landing_page", "")[:255] # Phase 2: Landing page URL
        ))
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": "Impression tracked successfully",
            "campaign_id": data["campaign_id"],
            "property_code": data["property_code"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to track impression: {str(e)}")


@router.post("/click") 
async def track_click(request: Request):
    """Track popup click event"""
    try:
        data = await request.json()
        
        # Basic validation
        required_fields = ["campaign_id", "property_code"]
        for field in required_fields:
            if field not in data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        conn = get_db_connection()
        
        # Insert click record with Phase 2 tracking
        conn.execute("""
            INSERT INTO clicks (
                campaign_id, property_code, session_id, placement,
                user_agent, timestamp, ip_hash, revenue_estimate,
                source, subsource, utm_campaign, referrer, landing_page
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["campaign_id"],
            data["property_code"],
            data.get("session_id", ""),
            data.get("placement", "thankyou"),
            data.get("user_agent", "")[:255],  # Limit user agent length
            data.get("timestamp", datetime.now().isoformat()),
            hash(str(request.client.host)) if request.client else 0,  # Simple IP hash
            0.45,  # Default estimated revenue (Mike's proven CPL)
            data.get("source", "")[:100],      # Phase 2: Traffic source
            data.get("subsource", "")[:100],   # Phase 2: Traffic subsource
            data.get("utm_campaign", "")[:100], # Phase 2: Campaign parameter
            data.get("referrer", "")[:255],    # Phase 2: Referrer URL
            data.get("landing_page", "")[:255] # Phase 2: Landing page URL
        ))
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": "Click tracked successfully",
            "campaign_id": data["campaign_id"],
            "property_code": data["property_code"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to track click: {str(e)}")

@router.get("/campaigns/{campaign_id}", response_model=Campaign)
async def get_campaign_by_id(campaign_id: int):
    """Get single campaign by ID"""
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            SELECT * FROM campaigns WHERE id = ?
        """, (campaign_id,))
        
        campaign = cursor.fetchone()
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        return dict(campaign)
    finally:
        conn.close()

@router.get("/campaigns/{campaign_id}/impression-pixel")
async def get_impression_pixel(campaign_id: int):
    """Generate Tune impression pixel for a campaign"""
    try:
        conn = get_db_connection()
        cursor = conn.execute("""
            SELECT offer_id, aff_id FROM campaigns WHERE id = ?
        """, (campaign_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        offer_id, aff_id = result
        
        if not offer_id or not aff_id:
            return {"pixel_url": None, "message": "Campaign missing offer_id or aff_id"}
        
        pixel_url = f"https://track.modemobile.com/aff_i?offer_id={offer_id}&aff_id={aff_id}"
        pixel_html = f'<img src="{pixel_url}" width="0" height="0" style="position:absolute;visibility:hidden;" border="0" />'
        
        return {
            "pixel_url": pixel_url,
            "pixel_html": pixel_html,
            "offer_id": offer_id,
            "aff_id": aff_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate impression pixel: {str(e)}")

@router.get("/analytics/attribution")
async def get_attribution_analytics():
    """Phase 2: Get traffic attribution analytics"""
    conn = get_db_connection()
    try:
        # Revenue by source
        cursor = conn.execute("""
            SELECT 
                COALESCE(source, 'Unknown') as source,
                COUNT(*) as clicks,
                SUM(revenue_estimate) as estimated_revenue,
                AVG(revenue_estimate) as avg_cpl
            FROM clicks 
            WHERE timestamp >= datetime('now', '-30 days')
            GROUP BY source
            ORDER BY estimated_revenue DESC
        """)
        source_data = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        
        # Revenue by subsource
        cursor = conn.execute("""
            SELECT 
                COALESCE(subsource, 'Unknown') as subsource,
                COUNT(*) as clicks,
                SUM(revenue_estimate) as estimated_revenue,
                AVG(revenue_estimate) as avg_cpl
            FROM clicks 
            WHERE timestamp >= datetime('now', '-30 days')
            GROUP BY subsource
            ORDER BY estimated_revenue DESC
        """)
        subsource_data = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        
        # Campaign performance with attribution (fixed to use impression source when click source missing)
        cursor = conn.execute("""
            SELECT 
                c.name as campaign_name,
                COALESCE(cl.source, i.source, 'Unknown') as source,
                COUNT(DISTINCT cl.id) as clicks,
                COUNT(DISTINCT i.id) as impressions,
                ROUND(CAST(COUNT(DISTINCT cl.id) AS FLOAT) / NULLIF(COUNT(DISTINCT i.id), 0) * 100, 2) as ctr,
                SUM(cl.revenue_estimate) as estimated_revenue
            FROM campaigns c
            LEFT JOIN clicks cl ON c.id = cl.campaign_id AND cl.timestamp >= datetime('now', '-30 days')
            LEFT JOIN impressions i ON c.id = i.campaign_id AND i.timestamp >= datetime('now', '-30 days')
            WHERE c.active = 1
            GROUP BY c.name, COALESCE(cl.source, i.source, 'Unknown')
            ORDER BY estimated_revenue DESC NULLS LAST
        """)
        campaign_data = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        
        return {
            "period": "Last 30 days", 
            "by_source": source_data,
            "by_subsource": subsource_data,
            "by_campaign": campaign_data,
            "summary": {
                "total_sources": len(source_data),
                "total_clicks": sum(item['clicks'] for item in source_data),
                "total_revenue": sum(item['estimated_revenue'] or 0 for item in source_data)
            }
        }
        
    finally:
        conn.close() 