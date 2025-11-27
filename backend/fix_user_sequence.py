"""
Fix PostgreSQL sequence for users table

This script resets the auto-increment sequence for the users table
to start from the correct number based on existing data.
"""

from database import engine
from sqlalchemy import text

def fix_user_sequence():
    """Reset the users table ID sequence"""
    with engine.connect() as conn:
        # Get the maximum ID currently in the users table
        result = conn.execute(text("SELECT MAX(id) FROM users"))
        max_id = result.fetchone()[0]
        
        if max_id is None:
            max_id = 0
        
        next_id = max_id + 1
        
        print(f"Current max user ID: {max_id}")
        print(f"Setting sequence to start at: {next_id}")
        
        # Reset the sequence
        conn.execute(text(f"SELECT setval('users_id_seq', {next_id}, false)"))
        conn.commit()
        
        print("[SUCCESS] User ID sequence reset successfully!")
        print(f"Next user will get ID: {next_id}")

if __name__ == "__main__":
    print("Fixing PostgreSQL user ID sequence...\n")
    fix_user_sequence()
