"""
Module for manage artists.
"""

from webargs.flaskparser import use_args
from flask import jsonify, request

from app import app, db
from app.models import (
    Artist,
    ArtistSchema,
    artist_schema,
)
from app.utils import validate_content_type


@app.route("/api/artists", methods=["GET"])
def get_artists():
    artists = Artist.query.all()
    artist_schema = ArtistSchema(many=True)
    return jsonify(
        {
            "success": True,
            "data": artist_schema.dump(artists),
            "number_of_records": len(artists),
        }
    )


@app.route("/api/artists/<int:artist_id>", methods=["GET"])
def get_artist_detail(artist_id: int):
    artist = Artist.query.get_or_404(
        artist_id, description=f"Artist with id {artist_id} not found."
    )
    return jsonify({"success": True, "data": artist_schema.dump(artist)})


@app.route("/api/artists", methods=["POST"])
@validate_content_type
@use_args(artist_schema, error_status_code=400)
def create_artist(args: dict):
    artist = Artist(**args)
    db.session.add(artist)
    db.session.commit()

    return (
        jsonify(
            {
                "success": True,
                "data": artist_schema.dump(artist),
            }
        ),
        201,
    )


@app.route("/api/artists/<int:artist_id>", methods=["PUT"])
@validate_content_type
@use_args(artist_schema, error_status_code=400)
def update_artist(args: dict, artist_id: int):
    artist = Artist.query.get_or_404(
        artist_id, description=f"Artist with id {artist_id} not found."
    )
    artist.name = args["name"]
    artist.label = args["label"]
    artist.birth_date = args["birth_date"]
    db.session.commit()

    return jsonify(
        {"success": True,
         "data": artist_schema.dump(artist)}
    )


@app.route("/api/artists/<int:artist_id>", methods=["DELETE"])
def delete_artist(artist_id: int):
    artist = Artist.query.get_or_404(
        artist_id, description=f"Artist with id {artist_id} not found."
    )
    db.session.delete(artist)
    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": f"Artist with id {artist_id} has been deleted.",
        }
    )
