"""
Sync users from SQLite (datasage_users.db) to PostgreSQL (DataSage_DataBase)

This script copies users from the SQLite authentication database
to the PostgreSQL users table so foreign key constraints work.
"""

import sqlite3
import sys
from database import SessionLocal
from models import User

def sync_users():
    """Copy users from SQLite to PostgreSQL"""
    
    # Connect to SQLite
    try:
        sqlite_conn = sqlite3.connect('datasage_users.db')
        sqlite_cursor = sqlite_conn.cursor()
        
        # Get all users from SQLite
        sqlite_cursor.execute("SELECT id, username, email, full_name, hashed_password FROM users")
        sqlite_users = sqlite_cursor.fetchall()
        
        print(f"Found {len(sqlite_users)} users in SQLite datasage_users.db")
        
    except Exception as e:
        print(f"Error reading from SQLite: {e}")
        return
    
    # Connect to PostgreSQL
    db = SessionLocal()
    
    try:
        synced = 0
        skipped = 0
        
        for user_data in sqlite_users:
            user_id, username, email, full_name, hashed_password = user_data
            
            # Check if user already exists in PostgreSQL
            existing_user = db.query(User).filter(User.id == user_id).first()
            
            if existing_user:
                print(f"  [SKIP] User {username} (ID: {user_id}) already exists in PostgreSQL")
                skipped += 1
                continue
            
            # Create new user in PostgreSQL
            new_user = User(
                id=user_id,
                username=username,
                email=email,
                full_name=full_name,
                hashed_password=hashed_password
            )
            
            db.add(new_user)
            print(f"  [OK] Synced user: {username} (ID: {user_id})")
            synced += 1
        
        # Commit all changes
        db.commit()
        
        print(f"\n[SUCCESS] Sync complete!")
        print(f"   Synced: {synced} users")
        print(f"   Skipped: {skipped} users (already existed)")
        
    except Exception as e:
        print(f"[ERROR] Error syncing to PostgreSQL: {e}")
        db.rollback()
    finally:
        db.close()
        sqlite_conn.close()

if __name__ == "__main__":
    print("Starting user sync from SQLite to PostgreSQL...\n")
    sync_users()
