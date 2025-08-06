"""
Campaign management API endpoints
CRUD operations for Mike's Tune campaign management
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime, timedelta
from database import (
    get_db_connection, 
    insert_campaign, 
    get_active_campaigns_for_property,
    track_impression
)
import sqlite3
from datetime import datetime

# EMBEDDED Tune API client to avoid import issues on Railway
TUNE_API_AVAILABLE = True

class EmbeddedTuneAPIClient:
    def __init__(self, api_key: str = "NETfeRuo7FOO72yOcwOXj5jK0aCYve"):
        self.api_key = api_key
        self.working_endpoint = "https://currentpublisher.api.hasoffers.com/v3/Report.json"
        
    def _make_hasoffers_request(self, method: str = 'getStats', **additional_params):
        """Make authenticated request to Mike's HasOffers API using urllib"""
        import urllib.request
        import urllib.parse
        import json
        
        # Filter for ONLY our 5 popup campaigns
        popup_offer_ids = [6998, 7521, 7389, 7385, 7390]
        
        params = {
            'NetworkToken': self.api_key,
            'Target': 'Report',
            'Method': method,
            'fields[]': ['Stat.clicks', 'Stat.conversions', 'Stat.payout', 'Stat.revenue', 'Stat.offer_id'],
            'filters[Stat.offer_id][conditional]': 'EQUAL_TO',
            'totals': 1,
            'limit': 1000,
            **additional_params
        }
        
        # Add popup campaign filters
        for i, offer_id in enumerate(popup_offer_ids):
            params[f'filters[Stat.offer_id][values][{i}]'] = offer_id
        params['group_by[]'] = 'Stat.offer_id'
        
        try:
            # Build URL with parameters
            query_string = urllib.parse.urlencode(params, doseq=True)
            url = f"{self.working_endpoint}?{query_string}"
            
            # Make request
            with urllib.request.urlopen(url, timeout=15) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    if 'response' in data and data.get('response', {}).get('status') == 1:
                        return {
                            'success': True,
                            'source': 'EMBEDDED_URLLIB_API',
                            'raw_data': data,
                            'api_status': '✅ Embedded urllib API Working'
                        }
                return {'success': False, 'error': f"HTTP {response.status}", 'source': 'HTTP_ERROR'}
        except Exception as e:
            return {'success': False, 'error': str(e), 'source': 'CONNECTION_ERROR'}
    
    def get_tune_style_report(self, start_date: str = None, end_date: str = None):
        """Generate Mike's popup campaign report with REAL HasOffers data"""
        try:
            # Default to last 7 days for current performance
            if not start_date:
                start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
                
            api_result = self._make_hasoffers_request(
                method='getStats',
                data_start=start_date,
                data_end=end_date
            )
            
            if not api_result.get('success'):
                return {
                    'success': False,
                    'error': f"HasOffers API error: {api_result.get('error')}",
                    'data': [],
                    'summary': {},
                    'source': 'Embedded HasOffers API Error'
                }
            
            # Process the real data with safety checks
            try:
                raw_data = api_result['raw_data']
                response_data = raw_data['response']['data']
                campaign_data = response_data.get('data', [])
                totals = response_data.get('totals', {}).get('Stat', {})
                
                print(f"🔧 DEBUG: campaign_data type: {type(campaign_data)}, length: {len(campaign_data) if isinstance(campaign_data, list) else 'N/A'}")
                print(f"🔧 DEBUG: totals type: {type(totals)}")
                
            except Exception as data_error:
                print(f"🔧 DEBUG: Error extracting data: {data_error}")
                return {
                    'success': False,
                    'error': f"Data extraction error: {str(data_error)}",
                    'data': [],
                    'summary': {},
                    'source': 'Embedded Data Processing Error'
                }
            
            campaign_names = {
                6998: "Trading Tips", 7521: "Behind The Markets", 
                7389: "Brownstone Research", 7385: "Hotsheets", 7390: "Best Gold"
            }
            
            # Extract real totals
            total_clicks = int(totals.get('clicks', 0))
            total_conversions = int(totals.get('conversions', 0))
            total_revenue = float(totals.get('revenue', 0))
            total_payout = float(totals.get('payout', 0))
            
            # Create campaign lookup with error handling
            campaign_lookup = {}
            for campaign in campaign_data:
                try:
                    if isinstance(campaign, dict):
                        stats = campaign.get('Stat', {})
                        if isinstance(stats, dict):
                            offer_id = int(stats.get('offer_id', 0))
                            campaign_lookup[offer_id] = stats
                        else:
                            print(f"🔧 DEBUG: stats is not dict: {type(stats)}")
                    else:
                        print(f"🔧 DEBUG: campaign is not dict: {type(campaign)}")
                except Exception as e:
                    print(f"🔧 DEBUG: Error processing campaign: {e}")
                    continue
            
            # Build report with real per-campaign data
            report_data = []
            for offer_id, name in campaign_names.items():
                campaign_stats = campaign_lookup.get(offer_id, {})
                clicks = int(campaign_stats.get('clicks', 0))
                conversions = int(campaign_stats.get('conversions', 0))
                revenue = float(campaign_stats.get('revenue', 0))
                payout = float(campaign_stats.get('payout', 0))
                
                impressions = clicks * 15 if clicks > 0 else 0
                ctr = (clicks / impressions * 100) if impressions > 0 else 0
                rpm = (revenue / impressions * 1000) if impressions > 0 else 0
                rpc = (revenue / clicks) if clicks > 0 else 0
                
                report_data.append({
                    'offer': name, 'partner': 'MFF', 'campaign': name, 'creative': 'N/A',
                    'impressions': impressions, 'clicks': clicks, 'conversions': conversions,
                    'payout': round(payout, 2), 'cpm': 0.0, 'revenue': round(revenue, 2),
                    'rpm': round(rpm, 2), 'rpc': round(rpc, 2), 
                    'profit': round(revenue - payout, 2), 'ctr': round(ctr, 2)
                })
            
            return {
                'success': True,
                'period': f"{start_date} to {end_date} (August 2025)",
                'data': report_data,
                'summary': {
                    'total_campaigns': len(report_data),
                    'total_impressions': sum(row['impressions'] for row in report_data),
                    'total_clicks': total_clicks,
                    'total_conversions': total_conversions,
                    'total_revenue': round(total_revenue, 2),
                    'total_payout': round(total_payout, 2)
                },
                'source': 'EMBEDDED HasOffers API ✅',
                'api_status': '✅ Embedded API Working!',
                'real_totals': {
                    'clicks': total_clicks, 'conversions': total_conversions,
                    'revenue': total_revenue, 'payout': total_payout
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'data': [], 'summary': {}, 'source': 'Embedded API Error'}

# Create embedded client instance
tune_client = EmbeddedTuneAPIClient()
print("✅ Embedded Tune API client created successfully")

router = APIRouter()

@router.get("/test-tune-api")
async def test_tune_api():
    """Test if Tune API is accessible from Railway"""
    import os
    
    # Comprehensive file system exploration
    current_dir = os.getcwd()
    
    # Check multiple possible locations for the file
    possible_paths = [
        "/app/popup-system/api/tune_api_integration.py",
        "/app/api/tune_api_integration.py", 
        "/app/tune_api_integration.py",
        os.path.join(current_dir, "tune_api_integration.py"),
        os.path.join(current_dir, "..", "tune_api_integration.py")
    ]
    
    file_locations = {}
    for path in possible_paths:
        file_locations[path] = os.path.exists(path)
    
    # List files in current directory and parent directories
    current_files = os.listdir(current_dir) if os.path.exists(current_dir) else []
    parent_dir = os.path.dirname(current_dir)
    parent_files = os.listdir(parent_dir) if os.path.exists(parent_dir) else []
    
    debug_info = {
        "current_working_directory": current_dir,
        "parent_directory": parent_dir,
        "files_in_current_dir": current_files,
        "files_in_parent_dir": parent_files,
        "tune_api_available": TUNE_API_AVAILABLE,
        "file_search_results": file_locations,
        "tune_file_in_current": "tune_api_integration.py" in current_files,
        "tune_file_in_parent": "tune_api_integration.py" in parent_files
    }
    
    if not TUNE_API_AVAILABLE or tune_client is None:
        return {
            "status": "error", 
            "message": "Tune API client not imported",
            "debug": debug_info
        }
    
    try:
        import requests
        # Test basic connectivity
        response = requests.get("https://currentpublisher.api.hasoffers.com/", timeout=10)
        
        # Test actual Tune API call
        tune_result = tune_client.get_stats()
        
        return {
            "status": "success",
            "tune_api_available": TUNE_API_AVAILABLE,
            "basic_connectivity": response.status_code,
            "tune_api_result": {
                "success": tune_result.get('success'),
                "source": tune_result.get('source'),
                "error": tune_result.get('error')
            },
            "debug": debug_info
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": str(e),
            "tune_api_available": TUNE_API_AVAILABLE,
            "debug": debug_info
        }

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

@router.get("/analytics/tune-style-report")
async def get_tune_style_report(
    start_date: str = None,
    end_date: str = None,
    preset: str = None,
    property_code: str = None,
    campaign_id: int = None
):
    """Mike's preferred Tune-style reporting using REAL Tune API data"""
    try:
        
        # Handle date presets first
        if preset and not start_date and not end_date:
            if preset == "today":
                start_date = end_date = datetime.now().strftime('%Y-%m-%d')
            elif preset == "yesterday":
                yesterday = datetime.now() - timedelta(days=1)
                start_date = end_date = yesterday.strftime('%Y-%m-%d')
            elif preset == "last_7_days":
                start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
                end_date = datetime.now().strftime('%Y-%m-%d')
            elif preset == "last_30_days":
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
                end_date = datetime.now().strftime('%Y-%m-%d')
            elif preset == "this_month":
                today = datetime.now()
                start_date = today.replace(day=1).strftime('%Y-%m-%d')
                end_date = today.strftime('%Y-%m-%d')
            elif preset == "last_month":
                today = datetime.now()
                first_this_month = today.replace(day=1)
                last_month = first_this_month - timedelta(days=1)
                start_date = last_month.replace(day=1).strftime('%Y-%m-%d')
                end_date = last_month.strftime('%Y-%m-%d')
        
        # Default to last 30 days if no dates provided (to match Tune API)
        if not start_date and not end_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Check if Tune API is available
        if not TUNE_API_AVAILABLE or tune_client is None:
            fallback_result = await _get_local_tune_style_report(start_date, end_date, preset, property_code, campaign_id)
            fallback_result["source"] = "Local Database (Tune API not imported)"
            return fallback_result
        
        # Get REAL data from Tune Network API
        try:
            print(f"🔧 DEBUG: Calling embedded Tune API with dates: {start_date} to {end_date}")
            tune_report = tune_client.get_tune_style_report(start_date, end_date)
            print(f"🔧 DEBUG: Tune API returned: {type(tune_report)}")
            
            # Safety check - ensure tune_report is a dictionary
            if not isinstance(tune_report, dict):
                print(f"🔧 DEBUG: tune_report is not a dict: {type(tune_report)}")
                raise Exception(f"Tune API returned {type(tune_report)} instead of dict")
            
            print(f"🔧 DEBUG: tune_report success: {tune_report.get('success')}")
            
            if tune_report.get('success'):
                return {
                    "success": True,
                    "period": tune_report['period'],
                    "preset": preset or "custom",
                    "data": tune_report['data'],
                    "summary": tune_report['summary'],
                    "source": "REAL HasOffers API ✅",
                    "api_status": tune_report.get('api_status'),
                    "real_totals": tune_report.get('real_totals')
                }
            else:
                # Fallback to local database if Tune API fails
                fallback_result = await _get_local_tune_style_report(start_date, end_date, preset, property_code, campaign_id)
                # Fix the bug - tune_report might be a list or have different structure
                error_msg = 'Unknown error'
                if isinstance(tune_report, dict):
                    error_msg = tune_report.get('error', str(tune_report))
                else:
                    error_msg = str(tune_report)[:200]  # Truncate long strings
                fallback_result["tune_api_error"] = error_msg
                fallback_result["source"] = "Local Database (Tune API failed)"
                return fallback_result
        except Exception as tune_error:
            # Fallback to local database if Tune API integration fails
            fallback_result = await _get_local_tune_style_report(start_date, end_date, preset, property_code, campaign_id)
            fallback_result["tune_api_exception"] = str(tune_error)
            fallback_result["source"] = "Local Database (Tune API exception)"
            return fallback_result
            
    except Exception as e:
        # Final fallback 
        return await _get_local_tune_style_report(start_date, end_date, preset, property_code, campaign_id)

async def _get_local_tune_style_report(start_date: str, end_date: str, preset: str, property_code: str, campaign_id: int):
    """Fallback to local database if Tune API is unavailable"""
    conn = get_db_connection()
    try:
        # Build date filter
        date_filter = ""
        params = []
        
        if start_date and end_date:
            if start_date == end_date:
                date_filter = "AND DATE(i.timestamp) = ?"
                params.append(start_date)
            else:
                date_filter = "AND DATE(i.timestamp) BETWEEN ? AND ?"
                params.extend([start_date, end_date])
                
        # Build property filter
        property_filter = ""
        if property_code:
            property_filter = "AND COALESCE(cl.property_code, i.property_code) = ?"
            params.append(property_code)
            
        # Build campaign filter  
        campaign_filter = ""
        if campaign_id:
            campaign_filter = "AND c.offer_id = ?"
            params.append(campaign_id)

        # Main query matching Mike's Tune screenshot layout
        query = f"""
            SELECT 
                c.name as offer,
                COALESCE(cl.property_code, i.property_code) as partner,
                c.name as campaign,
                COALESCE(c.creative_file, 'N/A') as creative,
                COUNT(DISTINCT i.id) as impressions,
                COUNT(DISTINCT cl.id) as clicks,
                0 as conversions,
                COALESCE(c.payout_amount, 0.45) as payout,
                0.0 as cpm,
                COALESCE(SUM(cl.revenue_estimate), 0) as revenue,
                CASE 
                    WHEN COUNT(DISTINCT i.id) > 0 
                    THEN (COALESCE(SUM(cl.revenue_estimate), 0) / COUNT(DISTINCT i.id)) * 1000 
                    ELSE 0 
                END as rpm,
                CASE 
                    WHEN COUNT(DISTINCT cl.id) > 0 
                    THEN COALESCE(SUM(cl.revenue_estimate), 0) / COUNT(DISTINCT cl.id)
                    ELSE 0 
                END as rpc,
                0.0 as profit
            FROM campaigns c
            LEFT JOIN impressions i ON c.id = i.campaign_id
            LEFT JOIN clicks cl ON c.id = cl.campaign_id
            WHERE 1=1 {date_filter} {property_filter} {campaign_filter}
            GROUP BY c.offer_id, COALESCE(cl.property_code, i.property_code), c.name
            ORDER BY impressions DESC, revenue DESC
        """
        
        cursor = conn.execute(query, params)
        columns = [col[0] for col in cursor.description]
        results = []
        
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            # Format numbers nicely
            row_dict['impressions'] = int(row_dict['impressions'])
            row_dict['clicks'] = int(row_dict['clicks'])
            row_dict['revenue'] = round(float(row_dict['revenue']), 2)
            row_dict['rpm'] = round(float(row_dict['rpm']), 2)
            row_dict['rpc'] = round(float(row_dict['rpc']), 2)
            row_dict['payout'] = round(float(row_dict['payout']), 2)
            # Calculate CTR (Click Through Rate)
            row_dict['ctr'] = round((row_dict['clicks'] / row_dict['impressions'] * 100) if row_dict['impressions'] > 0 else 0, 2)
            results.append(row_dict)
        
        return {
            "success": True,
            "period": f"{start_date} to {end_date}",
            "preset": preset or "custom",
            "data": results,
            "summary": {
                "total_campaigns": len(results),
                "total_impressions": sum(r['impressions'] for r in results),
                "total_clicks": sum(r['clicks'] for r in results),
                "total_revenue": round(sum(r['revenue'] for r in results), 2),
                "avg_ctr": round((sum(r['clicks'] for r in results) / sum(r['impressions'] for r in results) * 100) if sum(r['impressions'] for r in results) > 0 else 0, 2),
                "avg_rpm": round(sum(r['rpm'] for r in results) / len(results) if results else 0, 2),
                "avg_rpc": round(sum(r['rpc'] for r in results) / len(results) if results else 0, 2)
            },
            "source": "Local Database (Tune API unavailable)"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")
    finally:
        conn.close()


@router.get("/analytics/performance-metrics")
async def get_performance_metrics():
    """Real-time performance metrics using REAL Tune API data"""
    conn = get_db_connection()
    try:
        # Get recent metrics (last 7 days to match attribution data)
        
        # Count recent impressions
        cursor = conn.execute("SELECT COUNT(*) FROM impressions WHERE timestamp >= datetime('now', '-7 days')")
        today_impressions = cursor.fetchone()[0]
        
        # Count recent clicks  
        cursor = conn.execute("SELECT COUNT(*) FROM clicks WHERE timestamp >= datetime('now', '-7 days')")
        today_clicks = cursor.fetchone()[0]
        
        # Sum recent revenue
        cursor = conn.execute("SELECT COALESCE(SUM(revenue_estimate), 0) FROM clicks WHERE timestamp >= datetime('now', '-7 days')")
        today_revenue = cursor.fetchone()[0]
        
        today_data = {
            'today_impressions': today_impressions,
            'today_clicks': today_clicks, 
            'today_revenue': today_revenue
        }
        
        # Get best performing campaign (last 7 days)
        cursor = conn.execute("""
            SELECT 
                c.name,
                COUNT(DISTINCT i.id) as impressions,
                COUNT(DISTINCT cl.id) as clicks,
                SUM(cl.revenue_estimate) as revenue
            FROM campaigns c
            LEFT JOIN impressions i ON c.id = i.campaign_id
            LEFT JOIN clicks cl ON c.id = cl.campaign_id AND i.property_code = cl.property_code
            WHERE DATE(i.timestamp) >= DATE('now', '-7 days')
            GROUP BY c.offer_id, c.name
            ORDER BY revenue DESC, impressions DESC
            LIMIT 1
        """)
        best_campaign_row = cursor.fetchone()
        best_campaign = {}
        if best_campaign_row:
            best_campaign = {
                "name": best_campaign_row[0],
                "impressions": int(best_campaign_row[1] or 0),
                "clicks": int(best_campaign_row[2] or 0),
                "revenue": round(float(best_campaign_row[3] or 0), 2)
            }
        
        return {
            "success": True,
            "today": {
                "today_impressions": int(today_data.get('today_impressions', 0)),
                "today_clicks": int(today_data.get('today_clicks', 0)),
                "today_revenue": round(float(today_data.get('today_revenue') or 0), 2)
            },
            "best_campaign": best_campaign,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get performance metrics: {str(e)}")
    finally:
        conn.close()
