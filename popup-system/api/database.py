"""
Database setup for Mode Popup Management System
SQLite database with campaigns and property-specific settings
"""

import sqlite3
import os
from pathlib import Path

# Database file path - use persistent volume in production
DB_DIR = os.path.join(os.getcwd(), 'data')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "popup_campaigns.db")

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
                active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
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
        
        # Create simple impressions tracking table (minimal analytics)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS impressions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                property_code TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
            )
        """)
        
        # Create indexes for performance
        conn.execute("CREATE INDEX IF NOT EXISTS idx_campaign_active ON campaigns(active)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_property_active ON campaign_properties(property_code, active)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_impressions_date ON impressions(timestamp)")
        
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

def insert_campaign(name: str, tune_url: str, logo_url: str, main_image_url: str, description: str = ""):
    """Insert new campaign"""
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            INSERT INTO campaigns (name, tune_url, logo_url, main_image_url, description)
            VALUES (?, ?, ?, ?, ?)
        """, (name, tune_url, logo_url, main_image_url, description))
        
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