"""
Models in databse.
"""

from marshmallow import Schema, fields, validate, validates, ValidationError

from datetime import datetime

from app import db


class Artist(db.Model):
    """Model for artist"""

    __tablename__ = "Artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(50))
    birth_date = db.Column(db.Date)

    def __repr__(self):
        return f"<{self.__class__.__name__}>: {self.name}"


class ArtistSchema(Schema):
    """Class for serialization artists."""

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=50))
    label = fields.String(required=True, validate=validate.Length(max=50))
    birth_date = fields.Date("%d-%m-%Y", required=True)

    @validates("birth_date")
    def validate_birth_date(self, value):
        """Validation artist birth date."""
        today = datetime.now().date()
        if value > today:
            raise ValidationError(f"Birth date must be lower than {today}")
        return value

artist_schema = ArtistSchema()
