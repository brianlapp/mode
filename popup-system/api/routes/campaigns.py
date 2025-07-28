"""
Campaign management API endpoints
CRUD operations for Mike's Tune campaign management
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from database import (
    get_db_connection, 
    insert_campaign, 
    get_active_campaigns_for_property,
    track_impression
)
import sqlite3

router = APIRouter()

# Pydantic models for request/response
class CampaignCreate(BaseModel):
    name: str
    tune_url: str
    logo_url: str          # For top-left circle
    main_image_url: str    # For main offer display
    description: Optional[str] = ""

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    tune_url: Optional[str] = None
    logo_url: Optional[str] = None
    main_image_url: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None

class Campaign(BaseModel):
    id: int
    name: str
    tune_url: str
    logo_url: str
    main_image_url: str
    description: str
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

@router.get("/campaigns/{property_code}", response_model=List[CampaignForPopup])
async def get_campaigns_for_property(property_code: str):
    """Get active campaigns for specific property (for popup script)"""
    if property_code not in ['mff', 'mmm', 'mcad', 'mmd']:
        raise HTTPException(status_code=400, detail="Invalid property code")
    
    campaigns = get_active_campaigns_for_property(property_code)
    return campaigns

@router.post("/campaigns", response_model=dict)
async def create_campaign(campaign: CampaignCreate):
    """Create new campaign"""
    try:
        campaign_id = insert_campaign(
            name=campaign.name,
            tune_url=campaign.tune_url,
            logo_url=campaign.logo_url,
            main_image_url=campaign.main_image_url,
            description=campaign.description
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

@router.post("/impression", response_model=dict)
async def track_popup_impression(campaign_id: int, property_code: str):
    """Track when popup is shown to user"""
    if property_code not in ['mff', 'mmm', 'mcad', 'mmd']:
        raise HTTPException(status_code=400, detail="Invalid property code")
    
    try:
        track_impression(campaign_id, property_code)
        return {"status": "tracked"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

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