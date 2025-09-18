#!/usr/bin/env python3
"""
SQLite to PostgreSQL Migration Script
Safely migrates campaign data from SQLite backup to Railway PostgreSQL
"""

import sqlite3
import psycopg2
import os
from psycopg2.extras import RealDictCursor

# PostgreSQL connection from Railway
DATABASE_URL = "postgresql://postgres:oiOOYsoDLavzgajvmDXWnQsJsiKUxLsV@hopper.proxy.rlwy.net:59884/railway"
SQLITE_DB = "good_backup_database.db"

def migrate_data():
    print("🚀 Starting SQLite to PostgreSQL migration...")
    
    # Connect to SQLite
    sqlite_conn = sqlite3.connect(SQLITE_DB)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_conn.cursor()
    
    # Connect to PostgreSQL
    pg_conn = psycopg2.connect(DATABASE_URL)
    pg_cursor = pg_conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Get SQLite table structure
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in sqlite_cursor.fetchall()]
        print(f"📋 Found tables: {tables}")
        
        for table_name in tables:
            print(f"\n🔄 Migrating table: {table_name}")
            
            # Get table info
            sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
            columns_info = sqlite_cursor.fetchall()
            
            # Create PostgreSQL table
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
            column_defs = []
            
            for col in columns_info:
                col_name = col[1]
                col_type = col[2].upper()
                
                # Map SQLite types to PostgreSQL
                if col_type == "INTEGER":
                    pg_type = "INTEGER"
                elif col_type == "TEXT":
                    pg_type = "TEXT"
                elif col_type == "REAL":
                    pg_type = "DECIMAL(10,2)"
                elif col_type == "DATETIME":
                    pg_type = "TIMESTAMP"
                else:
                    pg_type = "TEXT"
                
                # Handle primary key
                if col[5]:  # is_pk
                    pg_type += " PRIMARY KEY"
                
                column_defs.append(f"{col_name} {pg_type}")
            
            create_table_sql += ", ".join(column_defs) + ");"
            
            print(f"📝 Creating table: {create_table_sql}")
            pg_cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            pg_cursor.execute(create_table_sql)
            
            # Get data from SQLite
            sqlite_cursor.execute(f"SELECT * FROM {table_name}")
            rows = sqlite_cursor.fetchall()
            
            if rows:
                # Prepare insert statement
                columns = [description[0] for description in sqlite_cursor.description]
                placeholders = ", ".join(["%s"] * len(columns))
                insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                
                # Insert data
                data_to_insert = [tuple(row) for row in rows]
                pg_cursor.executemany(insert_sql, data_to_insert)
                print(f"✅ Migrated {len(rows)} rows to {table_name}")
            else:
                print(f"⚠️  No data in {table_name}")
        
        # Commit changes
        pg_conn.commit()
        print("\n🎉 Migration completed successfully!")
        
        # Verify data
        print("\n📊 Verification:")
        for table_name in tables:
            pg_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = pg_cursor.fetchone()[0]
            print(f"  {table_name}: {count} rows")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        pg_conn.rollback()
        raise
    finally:
        sqlite_conn.close()
        pg_conn.close()

if __name__ == "__main__":
    migrate_data()
