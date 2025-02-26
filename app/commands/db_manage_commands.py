"""
Manage commands for db.
"""

from sqlalchemy.sql import text

import json
from pathlib import Path
from datetime import datetime

from app import db
from app.models import Artist, Album
from app.commands import db_manage_bp


def load_json_data(filename):
    """Loading json files."""
    json_path = Path(__file__).parent.parent / "samples" / filename
    with open(json_path) as file:
        data_json = json.load(file)
    return data_json


@db_manage_bp.cli.group()
def db_manage():
    """Database management commands."""
    pass


@db_manage.command()
def add_data():
    """Add sample data to database."""
    try:
        data_json = load_json_data("artists.json")
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

    try:
        data_json = load_json_data("albums.json")
        for item in data_json:
            album = Album(**item)
            db.session.add(album)
        db.session.commit()
        print("Data has been successfully added to database.")
    except Exception as e:
        print(f"Unexpected error: {e}")


@db_manage.command()
def remove_data():
    """Remove all data from database."""
    try:
        db.session.execute(text("DELETE FROM Albums"))
        db.session.execute(text("ALTER TABLE Albums AUTO_INCREMENT = 1"))
        db.session.execute(text("DELETE FROM Artists"))
        db.session.execute(text("ALTER TABLE Artists AUTO_INCREMENT = 1"))
        print("Data has been successfully removed from database.")
    except Exception as e:
        print(f"Unexpected error: {e}")
