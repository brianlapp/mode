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
            
        # Add featured priority field (FORCE FIX)
        try:
            conn.execute("ALTER TABLE campaigns ADD COLUMN featured BOOLEAN DEFAULT false")
            print("✅ Added featured priority field to campaigns table")
        except Exception as e:
            # Column already exists or other error - this is okay
            print(f"Featured column check: {e}")
            
        # Add updated_at column if missing (fix Railway startup error)
        try:
            conn.execute("ALTER TABLE campaigns ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("✅ Added updated_at column to campaigns table")
        except Exception as e:
            # Column already exists or other error - this is okay
            print(f"Updated_at column check: {e}")
            pass
            
        # Create properties table for multi-domain support
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,       -- 'mff', 'mmm', 'mcad', 'mmd'
                name TEXT NOT NULL,              -- 'ModeFreeFinds', etc.
                domain TEXT,                     -- e.g., 'modefreefinds.com'
                active BOOLEAN DEFAULT true,
                popup_enabled BOOLEAN DEFAULT true,
                popup_frequency TEXT DEFAULT 'session',   -- 'session', 'daily', 'always'
                popup_placement TEXT DEFAULT 'thankyou',  -- 'thankyou', 'exit-intent'
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Seed default properties if table empty
        cur = conn.execute("SELECT COUNT(1) FROM properties")
        if int(cur.fetchone()[0]) == 0:
            default_props = [
                ("mff", "ModeFreeFinds", "modefreefinds.com"),
                ("mmm", "ModeMarketMunchies", "modemarketmunchies.com"),
                ("mcad", "ModeClassActionsDaily", "modeclassactionsdaily.com"),
                ("mmd", "ModeMobileDaily", "modemobiledaily.com"),
            ]
            for code, name, domain in default_props:
                conn.execute(
                    "INSERT OR IGNORE INTO properties (code, name, domain, active, popup_enabled) VALUES (?, ?, ?, 1, 1)",
                    (code, name, domain),
                )

        # Ensure properties table has required columns
        try:
            cursor = conn.execute("PRAGMA table_info(properties)")
            prop_cols = [row[1] for row in cursor.fetchall()]
            if 'updated_at' not in prop_cols:
                conn.execute("ALTER TABLE properties ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                print("✅ Added updated_at column to properties table")
        except Exception as e:
            print(f"⚠️ Failed to ensure updated_at on properties: {e}")

        # Add featured_campaign_id column to properties table (for property-specific featured campaigns)
        try:
            conn.execute("ALTER TABLE properties ADD COLUMN featured_campaign_id INTEGER")
            print("✅ Added featured_campaign_id column to properties table")
        except Exception as e:
            # Column already exists or other error - this is okay
            pass

        # Create campaign_properties table for property-specific settings
        conn.execute("""
            CREATE TABLE IF NOT EXISTS campaign_properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                property_code TEXT NOT NULL,      -- 'mff', 'mmm', 'mcad', 'mmd'
                visibility_percentage INTEGER DEFAULT 100,  -- 0-100%
                active BOOLEAN DEFAULT true,
                impression_cap_daily INTEGER NULL, -- Daily impression cap (EST)
                click_cap_daily INTEGER NULL,      -- Daily click cap (EST)
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
                UNIQUE(campaign_id, property_code)  -- One setting per campaign per property
            )
        """)

        # Create properties table for multi-domain support
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,         -- 'mff', 'mmm', 'mcad', 'mmd'
                name TEXT NOT NULL,
                domain TEXT NOT NULL,             -- primary domain (used for resolve)
                active BOOLEAN DEFAULT 1,
                popup_enabled BOOLEAN DEFAULT 1,
                popup_frequency TEXT DEFAULT 'session', -- 'session' | 'daily' | 'always'
                popup_placement TEXT DEFAULT 'thankyou', -- 'thankyou' | 'exit-intent' | 'timed'
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Seed/update default properties (idempotent upserts by code)
        default_properties = [
            ("mff", "ModeFreeFinds", "modefreefinds.com"),
            ("mmm", "ModeMarketMunchies", "modemarketmunchies.com"),
            ("mcad", "ModeClassActionsDaily", "modeclassactionsdaily.com"),
            ("mmd", "ModeMobileDaily", "modemobiledaily.com"),
        ]
        for code, name, domain in default_properties:
            conn.execute(
                """
                INSERT INTO properties (code, name, domain, active, popup_enabled)
                VALUES (?, ?, ?, 1, 1)
                ON CONFLICT(code) DO UPDATE SET
                    name = excluded.name,
                    domain = excluded.domain,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (code, name, domain),
            )

        # Ensure cap columns exist for existing databases
        try:
            cursor = conn.execute("PRAGMA table_info(campaign_properties)")
            existing_columns = [row[1] for row in cursor.fetchall()]
            if 'impression_cap_daily' not in existing_columns:
                conn.execute("ALTER TABLE campaign_properties ADD COLUMN impression_cap_daily INTEGER")
                print("✅ Added impression_cap_daily to campaign_properties")
            if 'click_cap_daily' not in existing_columns:
                conn.execute("ALTER TABLE campaign_properties ADD COLUMN click_cap_daily INTEGER")
                print("✅ Added click_cap_daily to campaign_properties")
        except Exception as e:
            print(f"⚠️ Failed to add cap columns to campaign_properties: {e}")
        
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

        # Add daily cap columns to campaign_properties table if they don't exist
        cursor = conn.execute("PRAGMA table_info(campaign_properties)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        
        cap_columns = {
            'impression_cap_daily': 'INTEGER',
            'click_cap_daily': 'INTEGER'
        }
        
        for column, column_type in cap_columns.items():
            if column not in existing_columns:
                try:
                    conn.execute(f"ALTER TABLE campaign_properties ADD COLUMN {column} {column_type}")
                    print(f"✅ Added {column} to campaign_properties table")
                except Exception as e:
                    print(f"⚠️ Failed to add {column} to campaign_properties: {e}")
        
        print("✅ Daily cap columns verified/added to campaign_properties")

        # Add Mike's Tune-style reporting columns to campaigns table
        cursor = conn.execute("PRAGMA table_info(campaigns)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        
        reporting_columns = {
            'partner_name': 'TEXT',           # For Partner column in reports
            'advertiser_name': 'TEXT',        # For Advertiser column in reports  
            'payout_amount': 'DECIMAL(10,2) DEFAULT 0.45',  # For Payout column
            'creative_file': 'TEXT'           # For Creative column (filename)
        }
        
        for column, column_type in reporting_columns.items():
            if column not in existing_columns:
                try:
                    conn.execute(f"ALTER TABLE campaigns ADD COLUMN {column} {column_type}")
                    print(f"✅ Added {column} to campaigns table")
                except Exception as e:
                    print(f"⚠️ Failed to add {column} to campaigns: {e}")
        
        # Create conversions table for future Tune webhook integration
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                property_code TEXT NOT NULL,
                session_id TEXT,
                conversion_value DECIMAL(10,2) DEFAULT 0.45,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source TEXT,
                subsource TEXT,
                utm_campaign TEXT,
                referrer TEXT,
                landing_page TEXT,
                tune_conversion_id TEXT,  -- Tune's conversion ID from webhook
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
            )
        """)
        
        # Add indexes for Mike's reporting queries
        conn.execute("CREATE INDEX IF NOT EXISTS idx_conversions_campaign ON conversions(campaign_id, timestamp)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_conversions_property ON conversions(property_code, timestamp)")
        
        print("✅ Mike's attribution reporting columns verified/added")
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

def detect_property_code_from_host(hostname: str) -> str:
    """Resolve property_code from a given hostname using the properties table.
    Falls back to heuristic substring checks and defaults to 'mff'.
    """
    host = (hostname or "").lower()
    if not host:
        return "mff"

    conn = get_db_connection()
    try:
        # Exact domain match first
        cursor = conn.execute(
            "SELECT code FROM properties WHERE lower(domain) = ? AND active = 1",
            (host,),
        )
        row = cursor.fetchone()
        if row and row[0]:
            return row[0]

        # Substring match (e.g., subdomains)
        cursor = conn.execute("SELECT code, domain FROM properties WHERE active = 1")
        for r in cursor.fetchall():
            code, domain = r[0], (r[1] or "").lower()
            if domain and (domain in host or host.endswith("." + domain)):
                return code

    finally:
        conn.close()

    # Heuristic fallback
    if "modefreefinds" in host:
        return "mff"
    if "marketmunchies" in host:
        return "mmm"
    if "modeclassactions" in host:
        return "mcad"
    if "modemobiledaily" in host:
        return "mmd"
    return "mff"

def _get_est_day_bounds_sqlite_str():
    """Return (start_utc_str, end_utc_str) for current day in EST as 'YYYY-MM-DD HH:MM:SS' (UTC),
    which matches SQLite CURRENT_TIMESTAMP formatting for string comparisons."""
    from datetime import datetime, time, timedelta, timezone
    try:
        # Python 3.9+
        from zoneinfo import ZoneInfo  # type: ignore
        est = ZoneInfo("America/New_York")
        now_est = datetime.now(est)
        start_est = datetime.combine(now_est.date(), time.min, tzinfo=est)
        end_est = datetime.combine(now_est.date(), time.max, tzinfo=est)
        start_utc = start_est.astimezone(timezone.utc)
        end_utc = end_est.astimezone(timezone.utc)
    except Exception:
        # Fallback: approximate EST as UTC-5 (ignores DST)
        now_utc = datetime.utcnow().replace(tzinfo=timezone.utc)
        # Shift to EST (approx) then get date
        now_est = now_utc - timedelta(hours=5)
        start_est = datetime.combine(now_est.date(), time.min).replace(tzinfo=timezone.utc) + timedelta(hours=5)
        end_est = datetime.combine(now_est.date(), time.max).replace(tzinfo=timezone.utc) + timedelta(hours=5)
        start_utc = start_est - timedelta(hours=5)
        end_utc = end_est - timedelta(hours=5)

    # Format to SQLite CURRENT_TIMESTAMP-like string
    start_str = start_utc.replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    end_str = end_utc.replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    return start_str, end_str


def get_active_campaigns_for_property(property_code: str):
    """Get all active campaigns for a specific property, enforcing daily caps in EST."""
    conn = get_db_connection()
    try:
        # Check if daily cap columns exist first
        schema_cursor = conn.execute("PRAGMA table_info(campaign_properties)")
        columns = [row[1] for row in schema_cursor.fetchall()]
        has_cap_columns = 'impression_cap_daily' in columns and 'click_cap_daily' in columns
        
        if has_cap_columns:
            query = """
                SELECT 
                    c.id, c.name, c.tune_url, c.logo_url, c.main_image_url,
                    c.description, c.cta_text, c.offer_id, c.aff_id,
                    COALESCE(c.featured, 0) as featured,
                    cp.visibility_percentage,
                    COALESCE(cp.impression_cap_daily, NULL) as impression_cap_daily,
                    COALESCE(cp.click_cap_daily, NULL) as click_cap_daily
                FROM campaigns c
                JOIN campaign_properties cp ON c.id = cp.campaign_id
                WHERE c.active = 1 AND cp.active = 1 AND cp.property_code = ?
                ORDER BY COALESCE(c.featured, 0) DESC, c.created_at DESC
            """
        else:
            # Fallback query without cap columns
            query = """
                SELECT 
                    c.id, c.name, c.tune_url, c.logo_url, c.main_image_url,
                    c.description, c.cta_text, c.offer_id, c.aff_id,
                    COALESCE(c.featured, 0) as featured,
                    cp.visibility_percentage,
                    NULL as impression_cap_daily,
                    NULL as click_cap_daily
                FROM campaigns c
                JOIN campaign_properties cp ON c.id = cp.campaign_id
                WHERE c.active = 1 AND cp.active = 1 AND cp.property_code = ?
                ORDER BY COALESCE(c.featured, 0) DESC, c.created_at DESC
            """
        
        cursor = conn.execute(query, (property_code,))

        rows = [dict(row) for row in cursor.fetchall()]

        # Enforce caps for the current EST day
        start_str, end_str = _get_est_day_bounds_sqlite_str()
        eligible = []
        for row in rows:
            campaign_id = row["id"]
            # Count impressions today (EST window)
            imp_cap = row.get("impression_cap_daily")
            clk_cap = row.get("click_cap_daily")

            # Only query if a cap is set
            if imp_cap is not None:
                cur_imp = conn.execute(
                    """
                    SELECT COUNT(1) FROM impressions
                    WHERE campaign_id = ? AND property_code = ?
                      AND timestamp >= ? AND timestamp <= ?
                    """,
                    (campaign_id, property_code, start_str, end_str),
                )
                imp_count = int(cur_imp.fetchone()[0])
                if imp_count >= int(imp_cap):
                    # Skip campaign - impression cap reached
                    continue

            if clk_cap is not None:
                cur_clk = conn.execute(
                    """
                    SELECT COUNT(1) FROM clicks
                    WHERE campaign_id = ? AND property_code = ?
                      AND timestamp >= ? AND timestamp <= ?
                    """,
                    (campaign_id, property_code, start_str, end_str),
                )
                clk_count = int(cur_clk.fetchone()[0])
                if clk_count >= int(clk_cap):
                    # Skip campaign - click cap reached
                    continue

            # Apply visibility percentage filter
            visibility_pct = row.get("visibility_percentage", 100)
            if visibility_pct < 100:
                # Simple random-based approach for testing
                import random
                import time
                
                # Seed with campaign_id for some consistency within short timeframes
                random.seed(campaign_id * 1000 + int(time.time() // 300))  # Changes every 5 minutes
                random_pct = random.randint(0, 99)
                
                if random_pct >= visibility_pct:
                    # Skip this campaign - outside visibility percentage
                    continue

            eligible.append(row)

        return eligible
    finally:
        conn.close()


# Duplicate function removed - using the first implementation above

def insert_campaign(name: str, tune_url: str, logo_url: str, main_image_url: str, description: str = "", cta_text: str = "View Offer", offer_id: str = "", aff_id: str = "", featured: bool = False):
    """Insert new campaign with Tune tracking and priority support"""
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            INSERT INTO campaigns (name, tune_url, logo_url, main_image_url, description, cta_text, offer_id, aff_id, featured)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, tune_url, logo_url, main_image_url, description, cta_text, offer_id, aff_id, featured))
        
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