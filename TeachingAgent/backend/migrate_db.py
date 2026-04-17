#!/usr/bin/env python3
"""
Database migration script to add module organization fields
"""
import sqlite3
from pathlib import Path

def migrate_database():
    """Add new columns to concepts table"""
    db_path = Path(__file__).parent / "data" / "learning.db"
    
    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return
    
    print(f"🔧 Migrating database at {db_path}")
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(concepts)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # Add module column if it doesn't exist
        if 'module' not in columns:
            print("  ➕ Adding 'module' column...")
            cursor.execute("ALTER TABLE concepts ADD COLUMN module TEXT DEFAULT ''")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_concepts_module ON concepts(module)")
            print("  ✅ Added 'module' column")
        else:
            print("  ⏭️  'module' column already exists")
        
        # Add prerequisites_json column if it doesn't exist
        if 'prerequisites_json' not in columns:
            print("  ➕ Adding 'prerequisites_json' column...")
            cursor.execute("ALTER TABLE concepts ADD COLUMN prerequisites_json TEXT DEFAULT '[]'")
            print("  ✅ Added 'prerequisites_json' column")
        else:
            print("  ⏭️  'prerequisites_json' column already exists")
        
        # Add metadata_json column if it doesn't exist
        if 'metadata_json' not in columns:
            print("  ➕ Adding 'metadata_json' column...")
            cursor.execute("ALTER TABLE concepts ADD COLUMN metadata_json TEXT DEFAULT '{}'")
            print("  ✅ Added 'metadata_json' column")
        else:
            print("  ⏭️  'metadata_json' column already exists")
        
        conn.commit()
        print("\n🎉 Migration complete!")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()

# Made with Bob
