"""
Database setup for Mode Popup Management System
SQLite database with campaigns and property-specific settings
"""

import sqlite3
import os
from pathlib import Path

# Database file path - use persistent volume in production
def get_db_path():
    """Get database path with persistent volume support"""
    # Try persistent volume first (Railway production)
    volume_path = "/app/popup-system/api/data"
    if os.path.exists(volume_path):
        os.makedirs(volume_path, exist_ok=True)
        return os.path.join(volume_path, "popup_campaigns.db")
    
    # Secondary fallback for Railway
    fallback_path = "/app/api/data"
    if os.path.exists(fallback_path):
        os.makedirs(fallback_path, exist_ok=True)
        return os.path.join(fallback_path, "popup_campaigns.db")
    
    # Fallback to local path (development)
    return "popup_campaigns.db"

DB_PATH = get_db_path()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable dict-like access
    return conn

def init_db():
    """Initialize database with required tables"""
    conn = get_db_connection()
    
    try:
        # Create campaigns table with dual image support
        conn.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                tune_url TEXT NOT NULL,
                logo_url TEXT NOT NULL,           -- For top-left circle
                main_image_url TEXT NOT NULL,     -- For main offer display
                description TEXT,                 -- Optional campaign description
                cta_text TEXT DEFAULT 'View Offer', -- Customizable button text
                active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Add cta_text column if it doesn't exist (for existing databases)
        try:
            conn.execute("ALTER TABLE campaigns ADD COLUMN cta_text TEXT DEFAULT 'View Offer'")
            print("✅ Added cta_text column to existing campaigns table")
        except Exception as e:
            # Column already exists or other error - this is okay
            pass
            
        # Add impression pixel fields for Tune tracking
        try:
            conn.execute("ALTER TABLE campaigns ADD COLUMN offer_id TEXT")
            conn.execute("ALTER TABLE campaigns ADD COLUMN aff_id TEXT") 
            print("✅ Added Tune tracking fields (offer_id, aff_id) to campaigns table")
        except Exception as e:
            # Columns already exist or other error - this is okay
            pass
            
        # Create campaign_properties table for property-specific settings
        conn.execute("""
            CREATE TABLE IF NOT EXISTS campaign_properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                property_code TEXT NOT NULL,      -- 'mff', 'mmm', 'mcad', 'mmd'
                visibility_percentage INTEGER DEFAULT 100,  -- 0-100%
                active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
                UNIQUE(campaign_id, property_code)  -- One setting per campaign per property
            )
        """)
        
        # Create comprehensive impressions tracking table 
        conn.execute("""
            CREATE TABLE IF NOT EXISTS impressions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                property_code TEXT NOT NULL,
                session_id TEXT,
                placement TEXT DEFAULT 'thankyou',
                user_agent TEXT,
                ip_hash INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
            )
        """)
        
        # Create clicks tracking table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                property_code TEXT NOT NULL,
                session_id TEXT,
                placement TEXT DEFAULT 'thankyou',
                user_agent TEXT,
                ip_hash INTEGER,
                revenue_estimate DECIMAL(10,2) DEFAULT 0.45,
                conversion_tracked BOOLEAN DEFAULT false,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
            )
        """)
        
        # Add source/subsource tracking fields for Phase 2 attribution (AFTER tables exist)
        cursor = conn.execute("PRAGMA table_info(impressions)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        
        tracking_columns = ['source', 'subsource', 'utm_campaign', 'referrer', 'landing_page']
        for column in tracking_columns:
            if column not in existing_columns:
                try:
                    conn.execute(f"ALTER TABLE impressions ADD COLUMN {column} TEXT")
                    print(f"✅ Added {column} to impressions table")
                except Exception as e:
                    print(f"⚠️ Failed to add {column} to impressions: {e}")
        
        # Do the same for clicks table
        cursor = conn.execute("PRAGMA table_info(clicks)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        
        for column in tracking_columns:
            if column not in existing_columns:
                try:
                    conn.execute(f"ALTER TABLE clicks ADD COLUMN {column} TEXT")
                    print(f"✅ Added {column} to clicks table")
                except Exception as e:
                    print(f"⚠️ Failed to add {column} to clicks: {e}")
        
        print("✅ Phase 2 tracking fields verified/added")

        # Create indexes for performance
        conn.execute("CREATE INDEX IF NOT EXISTS idx_campaign_active ON campaigns(active)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_property_active ON campaign_properties(property_code, active)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_impressions_date ON impressions(timestamp)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_impressions_campaign ON impressions(campaign_id, timestamp)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_clicks_date ON clicks(timestamp)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_clicks_campaign ON clicks(campaign_id, timestamp)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_property_stats ON impressions(property_code, timestamp)")
        
        conn.commit()
        print("✅ Database initialized successfully")
        
    except sqlite3.Error as e:
        print(f"❌ Database initialization error: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_active_campaigns_for_property(property_code: str):
    """Get all active campaigns for a specific property"""
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
                c.cta_text,
                c.offer_id,
                c.aff_id,
                cp.visibility_percentage
            FROM campaigns c
            JOIN campaign_properties cp ON c.id = cp.campaign_id
            WHERE c.active = true 
            AND cp.active = true 
            AND cp.property_code = ?
            ORDER BY c.created_at DESC
        """, (property_code,))
        
        campaigns = [dict(row) for row in cursor.fetchall()]
        return campaigns
    finally:
        conn.close()

def insert_campaign(name: str, tune_url: str, logo_url: str, main_image_url: str, description: str = "", cta_text: str = "View Offer", offer_id: str = "", aff_id: str = ""):
    """Insert new campaign with Tune tracking support"""
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            INSERT INTO campaigns (name, tune_url, logo_url, main_image_url, description, cta_text, offer_id, aff_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, tune_url, logo_url, main_image_url, description, cta_text, offer_id, aff_id))
        
        campaign_id = cursor.lastrowid
        conn.commit()
        return campaign_id
    finally:
        conn.close()

def track_impression(campaign_id: int, property_code: str):
    """Track popup impression"""
    conn = get_db_connection()
    try:
        conn.execute("""
            INSERT INTO impressions (campaign_id, property_code)
            VALUES (?, ?)
        """, (campaign_id, property_code))
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    # Initialize database when run directly
    init_db() 