# Create a reset script: reset_db.py
from app import create_app, db

app = create_app()
with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    print("All tables dropped!")
    
from app import create_app, db
import sqlalchemy as sa

app = create_app()
with app.app_context():
    # Get engine
    engine = db.engine
    
    # Drop ALL tables
    db.drop_all()
    
    # Explicitly drop alembic_version if it exists
    with engine.connect() as conn:
        # Check if alembic_version table exists
        inspector = sa.inspect(engine)
        if 'alembic_version' in inspector.get_table_names():
            conn.execute(sa.text('DROP TABLE alembic_version'))
            print("Dropped alembic_version table")
    
    print("✅ All tables dropped including alembic_version")