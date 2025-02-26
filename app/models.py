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
    album = db.relationship(
        "Album", back_populates="artist", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}>: {self.name}"

    @staticmethod
    def additional_validate(param, value):
        if param == "birth_date":
            try:
                value = datetime.strptime(value, "%d-%m-%Y").date()
            except ValueError:
                value = None
        return value


class Album(db.Model):
    """Model for music albums."""

    __tablename__ = "Albums"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    number_of_songs = db.Column(db.Integer)
    description = db.Column(db.Text)
    release_year = db.Column(db.Integer)
    artist_id = db.Column(
        db.Integer,
        db.ForeignKey("Artists.id"),
        nullable=False
    )
    artist = db.relationship("Artist", back_populates="album")

    def __repr__(self):
        return f"{self.title} - {self.artist.name} ({self.release_year})"


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
