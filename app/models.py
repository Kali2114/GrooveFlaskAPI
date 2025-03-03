"""
Models in databse.
"""

import jwt
from flask import current_app
from marshmallow import (
    Schema,
    fields,
    validate,
    validates,
    validates_schema,
    ValidationError,
)

from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Artist(db.Model):
    """Model for artist"""

    __tablename__ = "Artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    albums = db.relationship(
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
    artist_id = db.Column(db.Integer, db.ForeignKey("Artists.id"), nullable=False)
    artist = db.relationship("Artist", back_populates="albums")

    def __repr__(self):
        return f"{self.title} - {self.artist.name} ({self.release_year})"

    @staticmethod
    def additional_validate(param, value):
        return value


class User(db.Model):
    """Model for users."""

    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.now)

    @staticmethod
    def generate_hashed_password(password):
        """Generate hashed password for user."""
        return generate_password_hash(password)

    def generate_jwt(self):
        """Generate JWT Token for user."""
        payload = {
            "user_id": self.id,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=current_app.config.get("JWT_EXPIRED_MINUTES", 60)),
        }
        return jwt.encode(payload, current_app.config.get("SECRET_KEY"))

    def is_password_valid(self, password):
        """Check that the password to login is valid."""
        return check_password_hash(self.password, password)


class ArtistSchema(Schema):
    """Class for serialization artists."""

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=50))
    label = fields.String(required=True, validate=validate.Length(max=50))
    birth_date = fields.Date("%d-%m-%Y", required=True)
    albums = fields.List(fields.Nested(lambda: AlbumSchema(exclude=["artist"])))

    @validates("birth_date")
    def validate_birth_date(self, value):
        """Validation artist birth date."""
        today = datetime.now().date()
        if value > today:
            raise ValidationError(f"Birth date must be lower than {today}")
        return value


class AlbumSchema(Schema):
    """Class for serialization albums."""

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(max=50))
    number_of_songs = fields.Integer(required=True)
    description = fields.String()
    release_year = fields.Integer(required=True)
    artist_id = fields.Integer(load_only=True)
    artist = fields.Nested(lambda: ArtistSchema(only=["id", "name", "label"]))

    @validates_schema(skip_on_field_errors=False)
    def validate_album(self, data, **kwargs):
        """Validation that number of songs and release
        year must be greater than zero."""
        if "number_of_songs" in data and data["number_of_songs"] <= 0:
            raise ValidationError("Number of songs must be greater than zero.")

        if "release_year" in data and data["release_year"] <= 0:
            raise ValidationError("Release year must be greater than zero.")


class UserSchema(Schema):
    """Class for serialization user."""

    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(max=255))
    email = fields.Email(required=True)
    password = fields.String(
        required=True, load_only=True, validate=validate.Length(min=6, max=255)
    )
    creation_date = fields.DateTime(dump_only=True)


artist_schema = ArtistSchema()
album_schema = AlbumSchema()
user_schema = UserSchema()
