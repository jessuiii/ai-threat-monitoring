import os
import sys
from sqlalchemy import text

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine
from app.models import Base, NetworkEvent

def upgrade_database():
    print("🔄 Connecting to Database...")
    
    with engine.connect() as conn:
        print("💥 Dropping old 'network_events' table...")
        # Use text() explicitly for the SQL statement
        conn.execute(text("DROP TABLE IF EXISTS network_events CASCADE;"))
        conn.commit()
        print("✅ Table dropped.")

    print("🏗️  Recreating tables with new schema...")
    # This will create network_events with the new 'service' column
    Base.metadata.create_all(bind=engine)
    print("✅ Database schema updated successfully!")

if __name__ == "__main__":
    upgrade_database()
