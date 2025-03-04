"""
Module for manage artists.
"""

from webargs.flaskparser import use_args
from flask import jsonify

from app import db
from app.models import (
    Artist,
    ArtistSchema,
    artist_schema,
)
from app.utils import (
    validate_content_type,
    get_schema_args,
    apply_orders,
    apply_filter,
    get_pagination,
    token_required,
)
from app.artists import artists_bp


@artists_bp.route("/artists", methods=["GET"])
def get_artists():
    query = Artist.query
    schema_args = get_schema_args(Artist)
    query = apply_orders(Artist, query)
    query = apply_filter(Artist, query)
    items, pagination = get_pagination(query, "artists.get_artists")
    artists = ArtistSchema(**schema_args).dump(items)

    return jsonify(
        {
            "success": True,
            "data": artists,
            "number_of_records": len(artists),
            "pagination": pagination,
        }
    )


@artists_bp.route("/artists/<int:artist_id>", methods=["GET"])
def get_artist_detail(artist_id: int):
    artist = Artist.query.get_or_404(
        artist_id, description=f"Artist with id {artist_id} not found."
    )
    return jsonify({"success": True, "data": artist_schema.dump(artist)})


@artists_bp.route("/artists", methods=["POST"])
@token_required
@validate_content_type
@use_args(artist_schema, error_status_code=400)
def create_artist(user_id: int, args: dict):
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


@artists_bp.route("/artists/<int:artist_id>", methods=["PUT"])
@token_required
@validate_content_type
@use_args(artist_schema, error_status_code=400)
def update_artist(user_id: int, args: dict, artist_id: int):
    artist = Artist.query.get_or_404(
        artist_id, description=f"Artist with id {artist_id} not found."
    )
    artist.name = args["name"]
    artist.label = args["label"]
    artist.birth_date = args["birth_date"]
    db.session.commit()

    return jsonify({"success": True, "data": artist_schema.dump(artist)})


@artists_bp.route("/artists/<int:artist_id>", methods=["DELETE"])
@token_required
def delete_artist(user_id: int, artist_id: int):
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
