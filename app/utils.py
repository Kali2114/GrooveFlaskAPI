"""
Utils for app.
"""

from flask import (
    request,
    url_for,
    current_app,
    abort,
)

import jwt
from werkzeug.exceptions import UnsupportedMediaType
from functools import wraps
import re


COMPARISON_OPERATORS_RE = re.compile(r"(.*)\[(gte|gt|lte|lt)]")


def validate_content_type(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        if data is None:
            raise UnsupportedMediaType("Content type must be application/json")
        return func(*args, **kwargs)

    return wrapper


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        auth = request.headers.get("Authorization")
        if auth:
            token = auth.split(" ")[1]
        if token is None:
            abort(401, description="Missing token. Please login or register.")

        try:
            payload = jwt.decode(
                token, current_app.config.get("SECRET_KEY"), algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            abort(401, description="Expired token. Please login to get new token.")
        except jwt.InvalidTokenError:
            abort(401, description="Invalid token. Please login or register.")
        else:
            return func(payload["user_id"], *args, **kwargs)

    return wrapper


def get_schema_args(model):
    """Returns schema arguments with optional field filtering."""
    schema_args = {"many": True}
    fields = request.args.get("fields")
    if fields:
        schema_args["only"] = [
            field for field in fields.split(",") if field in model.__table__.columns
        ]
    return schema_args


def apply_orders(model, query):
    """Applies sorting to the query based on provided sort keys."""
    sort_keys = request.args.get("sort")
    if sort_keys:
        for key in sort_keys.split(","):
            flag = False
            if key.startswith("-"):
                key = key[1:]
                flag = True
            column_attr = getattr(model, key, None)
            if column_attr is not None:
                query = (
                    query.order_by(column_attr.desc())
                    if flag
                    else query.order_by(column_attr)
                )
    return query


def _get_filter_argument(column_name, value, operator):
    operator_mapping = {
        "==": column_name == value,
        "gte": column_name >= value,
        "gt": column_name > value,
        "lte": column_name <= value,
        "lt": column_name < value,
    }
    return operator_mapping[operator]


def apply_filter(model, query):
    """Apply filter to records."""
    for param, value in request.args.items():
        if param not in {"fields", "sort", "page", "limit"}:
            operator = "=="
            match = COMPARISON_OPERATORS_RE.match(param)
            if match is not None:
                param, operator = match.groups()
            column_attr = getattr(model, param, None)
            if column_attr is not None:
                value = model.additional_validate(param, value)
                if value is None:
                    continue
                filter_argument = _get_filter_argument(column_attr, value, operator)
                query = query.filter(filter_argument)
    return query


def get_pagination(query, func_name):
    """Apply pagination to records."""
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", current_app.config.get("PER_PAGE", 5), type=int)
    params = {key: value for key, value in request.args.items() if key != "page"}
    paginate_obj = query.paginate(page=page, per_page=limit, error_out=False)
    pagination = {
        "total_pages": paginate_obj.pages,
        "total_records": paginate_obj.total,
        "current_page": url_for(func_name, page=page, **params),
    }
    if paginate_obj.has_next:
        pagination["next_page"] = url_for(func_name, page=page + 1, **params)

    if paginate_obj.has_prev:
        pagination["previous_page"] = url_for(func_name, page=page - 1, **params)

    return paginate_obj.items, pagination


def check_exists(model, args):
    if model.query.filter(model.username == args["username"]).first():
        abort(409, description=f"User with username {args['username']} already exists.")
    if model.query.filter(model.email == args["email"]).first():
        abort(409, description=f"User with email {args['email']} already exists.")
