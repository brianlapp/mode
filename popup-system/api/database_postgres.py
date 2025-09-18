"""
Database setup for Mode Popup Management System
PostgreSQL database with campaigns and property-specific settings
"""

import psycopg2
import psycopg2.extras
import os
from contextlib import contextmanager

# PostgreSQL connection from Railway environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Handle Railway's postgres:// vs postgresql:// URL format
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if not DATABASE_URL:
    # Fallback to SQLite for local development
    import sqlite3
    from pathlib import Path
    
    def get_db_path():
        return "popup_campaigns.db"
    
    DB_PATH = get_db_path()
    
    def get_db_connection():
        """Get SQLite connection for local development"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    
    # Use original SQLite init_db function
    from database import init_db
    
else:
    # PostgreSQL connection - compatible with existing SQLite code
    def get_db_connection():
        """Get PostgreSQL connection (non-context manager for compatibility)"""
        conn = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        return conn
    
    # Also provide context manager version for new code
    @contextmanager
    def get_db_connection_ctx():
        """Get PostgreSQL connection with context manager"""
        conn = None
        try:
            conn = psycopg2.connect(
                DATABASE_URL,
                cursor_factory=psycopg2.extras.RealDictCursor
            )
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    def init_db():
        """Initialize PostgreSQL database - schema should already exist from migration"""
        print("🐘 Using PostgreSQL database")
        
        # Test connection
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM campaigns")
            count = cursor.fetchone()[0]
            print(f"✅ PostgreSQL connected - {count} campaigns found")
            conn.close()
            return True
        except Exception as e:
            print(f"❌ PostgreSQL connection failed: {e}")
            return False

# Compatibility functions for existing code
def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """Execute query with PostgreSQL or SQLite compatibility"""
    if DATABASE_URL:
        # PostgreSQL
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                
                if fetch_one:
                    return cursor.fetchone()
                elif fetch_all:
                    return cursor.fetchall()
                else:
                    conn.commit()
                    return cursor.rowcount
    else:
        # SQLite fallback
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.rowcount
        finally:
            conn.close()

def get_campaigns_for_property(property_code):
    """Get campaigns for a specific property"""
    query = """
        SELECT c.* FROM campaigns c
        JOIN campaign_properties cp ON c.id = cp.campaign_id
        WHERE cp.property_code = %s AND c.active = true AND cp.active = true
        ORDER BY cp.weight DESC, c.id
    """
    return execute_query(query, (property_code,), fetch_all=True)

def track_impression(offer_id, property_code, source='popup', **kwargs):
    """Track impression in PostgreSQL"""
    query = """
        INSERT INTO impressions (offer_id, property_code, source, subsource, session_id, 
                               utm_campaign, utm_source, utm_medium, referrer, landing_page,
                               user_agent, ip_address, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    params = (
        offer_id, property_code, source,
        kwargs.get('subsource'), kwargs.get('session_id'),
        kwargs.get('utm_campaign'), kwargs.get('utm_source'), kwargs.get('utm_medium'),
        kwargs.get('referrer'), kwargs.get('landing_page'),
        kwargs.get('user_agent'), kwargs.get('ip_address')
    )
    return execute_query(query, params)

def track_click(offer_id, property_code, source='popup', **kwargs):
    """Track click in PostgreSQL"""
    query = """
        INSERT INTO clicks (offer_id, property_code, source, subsource, session_id,
                          utm_campaign, utm_source, utm_medium, referrer, landing_page,
                          user_agent, ip_address, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    params = (
        offer_id, property_code, source,
        kwargs.get('subsource'), kwargs.get('session_id'),
        kwargs.get('utm_campaign'), kwargs.get('utm_source'), kwargs.get('utm_medium'),
        kwargs.get('referrer'), kwargs.get('landing_page'),
        kwargs.get('user_agent'), kwargs.get('ip_address')
    )
    return execute_query(query, params)
