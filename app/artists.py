"""
Module for manage artists.
"""

from flask import jsonify

from app import app

@app.route("/api/artists", methods=["GET"])
def get_artists():
    return jsonify({
        "success": True,
        "data": "Eminem",
    })


@app.route("/api/artists/<int:artist_id>", methods=["GET"])
def get_artist_detail(artist_id: int):
    return jsonify({
        "success": True,
        "data": f"Artist with id {artist_id}.",
    })

@app.route("/api/artists", methods=["POST"])
def create_artis():
    return jsonify({
        "success": True,
        "data": "New artist create!",
    }), 201

@app.route("/api/artists/<int:artist_id>", methods=["PUT"])
def update_artist(artist_id: int):
    return jsonify({
        "success": True,
        "data": f"Artist with id {artist_id} has been updated."
    })

@app.route("/api/artists/<int:artist_id>", methods=["DELETE"])
def delete_artist(artist_id: int):
    return jsonify({
        "success": True,
        "data": f"Artist with id {artist_id} has been deleted.",
    })
