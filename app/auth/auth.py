"""
Authorization for app.
"""

from flask import abort, jsonify
from webargs.flaskparser import use_args

from app import db
from app.auth import auth_bp
from app.models import (
    user_schema,
    User,
    UserSchema,
    user_password_update,
)
from app.utils import validate_content_type, token_required, check_exists


@auth_bp.route("/register", methods=["POST"])
@validate_content_type
@use_args(user_schema, error_status_code=400)
def register(args: dict):
    """Register a new user."""
    if User.query.filter(User.username == args["username"]).first():
        abort(409, description=f"User with username {args['username']} already exists.")
    if User.query.filter(User.email == args["email"]).first():
        abort(409, description=f"User with email {args['email']} already exists.")

    args["password"] = User.generate_hashed_password(args["password"])
    user = User(**args)
    db.session.add(user)
    db.session.commit()
    token = user.generate_jwt()

    return jsonify({"success": True, "token": token}), 201


@auth_bp.route("/login", methods=["POST"])
@validate_content_type
@use_args(UserSchema(only=["username", "password"]))
def login(args: dict):
    user = User.query.filter(User.username == args["username"]).first()
    if not user:
        abort(401, description="Invalid user")
    if not user.is_password_valid(args["password"]):
        abort(401, description="Invalid password")

    token = user.generate_jwt()

    return jsonify({"success": True, "token": token})


@auth_bp.route("/me", methods=["GET"])
@token_required
def get_current_user(user_id):
    user = User.query.get_or_404(
        user_id, description=f"User with id {user_id} not found"
    )
    return jsonify({"success": True, "data": user_schema.dump(user)})


@auth_bp.route("/update/password", methods=["PUT"])
@token_required
@validate_content_type
@use_args(user_password_update, error_status_code=400)
def get_update_user_password(user_id, args):
    user = User.query.get_or_404(
        user_id, description=f"User with id {user_id} not found"
    )
    if not user.is_password_valid(args["current_password"]):
        abort(401, description="Invalid password.")

    user.password = user.generate_hashed_password(args["new_password"])
    db.session.commit()

    return jsonify({"success": True, "data": user_schema.dump(user)})


@auth_bp.route("/update/data", methods=["PUT"])
@token_required
@validate_content_type
@use_args(UserSchema(only=["username", "email"]), error_status_code=400)
def get_update_user_data(user_id, args):
    check_exists(User, args)
    user = User.query.get_or_404(
        user_id, description=f"User with id {user_id} not found"
    )
    user.username = args["username"]
    user.email = args["email"]
    db.session.commit()

    return jsonify({"success": True, "data": user_schema.dump(user)})
