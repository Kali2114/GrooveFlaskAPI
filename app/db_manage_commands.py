"""
Manage commands for db.
"""

from sqlalchemy.sql import text

import json
from pathlib import Path
from datetime import datetime

from app import app, db
from app.models import Artist


@app.cli.group()
def db_manage():
    """Database management commands."""
    pass


@db_manage.command()
def add_data():
    """Add sample data to database."""
    try:
        artists_path = Path(__file__).parent / "samples" / "artists.json"
        with open(artists_path) as file:
            data_json = json.load(file)
        for item in data_json:
            item["birth_date"] = datetime.strptime(
                item["birth_date"], "%d-%m-%Y"
            ).date()
            artist = Artist(**item)
            db.session.add(artist)
        db.session.commit()
        print("Data has been successfully added to database.")
    except Exception as e:
        print(f"Unexpected error: {e}")


@db_manage.command()
def remove_data():
    """Remove all data from database."""
    try:
        db.session.execute(text("TRUNCATE TABLE Artists"))
        db.session.commit()
        print("Data has been successfully removed from database.")
    except Exception as e:
        print(f"Unexpected error: {e}")
