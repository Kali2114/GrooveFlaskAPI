"""
Module for manage albums.
"""

from webargs.flaskparser import use_args
from flask import jsonify, request

from app import db
from app.models import (
    Album,
    AlbumSchema,
    album_schema,
    Artist,
)
from app.utils import (
    validate_content_type,
    get_schema_args,
    apply_orders,
    apply_filter,
    get_pagination,
)
from app.albums import albums_bp


@albums_bp.route("/albums", methods=["GET"])
def get_albums():
    query = Album.query
    schema_args = get_schema_args(album_schema)
    query = apply_orders(Album, query)
    query = apply_filter(Album, query)
    items, pagination = get_pagination(query, "albums.get_albums")
    albums = AlbumSchema(**schema_args).dump(items)

    return jsonify(
        {
            "success": True,
            "data": albums,
            "number_of_records": len(albums),
            "pagination": pagination,
        }
    )


@albums_bp.route("/albums/<int:album_id>", methods=["GET"])
def get_album_detail(album_id: int):
    album = Album.query.get_or_404(
        album_id, description=f"Album with id {album_id} not found."
    )
    return jsonify({"Success": True, "data": album_schema.dump(album)})


@albums_bp.route("/albums/<int:album_id>", methods=["PUT"])
@validate_content_type
@use_args(album_schema, error_status_code=400)
def update_album(args: dict, album_id: int):
    print("Received args:", args)
    print("Received raw request JSON:", request.get_json())
    print("Received args:", args)

    if not args:
        return jsonify({"error": "No valid data received"}), 400
    album = Album.query.get_or_404(
        album_id, description=f"Album with id {album_id} not found."
    )

    album.title = args["title"]
    album.number_of_songs = args["number_of_songs"]
    album.description = args["description"]
    album.release_year = args["release_year"]
    db.session.commit()

    return jsonify({"success": True, "data": album_schema.dump(album)})


@albums_bp.route("albums/<int:album_id>", methods=["DELETE"])
def delete_artist(album_id: int):
    album = Album.query.get_or_404(
        album_id, description=f"Album with id {album_id} not found."
    )
    db.session.delete(album)
    db.session.commit()

    return jsonify(
        {
            "success": True,
            "data": f"Album with id {album_id} has been deleted."
         }
    )


@albums_bp.route("artists/<int:artist_id>/albums", methods=["GET"])
def get_all_artist_albums(artist_id):
    Artist.query.get_or_404(
        artist_id, description=f"Artist with id {artist_id} not found."
    )
    albums = Album.query.filter(Album.artist_id == artist_id).all()
    items = AlbumSchema(many=True, exclude=["artist"]).dump(albums)

    return jsonify({"success": True, "data": items, "number_of_records": len(items)})


@albums_bp.route("artist/<int:artist_id>/albums", methods=["POST"])
@validate_content_type
@use_args(AlbumSchema(exclude=["artist_id"]), error_status_code=400)
def create_album(args: dict, artist_id: int):
    Artist.query.get_or_404(
        artist_id, description=f"Artist with id {artist_id} not found."
    )
    album = Album(artist_id=artist_id, **args)
    db.session.add(album)
    db.session.commit()

    return jsonify({"success": True, "data": album_schema.dump(album)}), 201
