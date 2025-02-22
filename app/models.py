"""
Models in databse.
"""
from marshmallow import Schema, fields, validate, validates, ValidationError
from flask import request, url_for

import re
from datetime import datetime

from app import db
from app import Config


COMPARISON_OPERATORS_RE = re.compile(r'(.*)\[(gte|gt|lte|lt)]')


class Artist(db.Model):
    """Model for artist"""

    __tablename__ = "Artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(50))
    birth_date = db.Column(db.Date)

    def __repr__(self):
        return f"<{self.__class__.__name__}>: {self.name}"

    @staticmethod
    def get_schema_args(fields: str) -> dict:
        """Returns schema arguments with optional field filtering."""
        schema_args = {"many": True}
        if fields:
            schema_args["only"] = [
                field for field in fields.split(",") if field in Artist.__table__.columns
            ]
        return schema_args

    @staticmethod
    def apply_orders(query, sort_keys):
        """Applies sorting to the query based on provided sort keys."""
        if sort_keys:
            for key in sort_keys.split(','):
                flag = False
                if key.startswith("-"):
                    key = key[1:]
                    flag = True
                column_attr = getattr(Artist, key, None)
                if column_attr is not None:
                    query = query.order_by(column_attr.desc()) if flag else query.order_by(column_attr)
        return query

    @staticmethod
    def get_filter_argument(column_name, value, operator):
        operator_mapping = {
            "==": column_name == value,
            "gte": column_name >= value,
            "gt": column_name > value,
            "lte": column_name <= value,
            "lt": column_name < value,
        }
        return operator_mapping[operator]

    @staticmethod
    def apply_filter(query):
        """Apply filter to records."""
        for param, value in request.args.items():
            if param not in {"fields", "sort", "page", "limit"}:
                operator = "=="
                match = COMPARISON_OPERATORS_RE.match(param)
                if match is not None:
                    param, operator = match.groups()
                column_attr = getattr(Artist, param, None)
                if column_attr is not None:
                    if param == "birth_date":
                        try:
                            value = datetime.strptime(value, "%d-%m-%Y").date()
                        except ValueError:
                            continue
                    filter_argument = Artist.get_filter_argument(column_attr, value, operator)
                    query = query.filter(filter_argument)
        return query

    @staticmethod
    def get_pagination(query):
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", Config.PER_PAGE, type=int)
        params = {key: value for key, value in request.args.items() if key != "page"}
        paginate_obj = query.paginate(page=page, per_page=limit, error_out=False)
        pagination = {
            "total_pages": paginate_obj.pages,
            "total_records": paginate_obj.total,
            "current_page": url_for("artists.get_artists", page=page, **params)
        }
        if paginate_obj.has_next:
            pagination["next_page"] = url_for("artists.get_artists", page=page+1, **params)

        if paginate_obj.has_prev:
            pagination["previous_page"] = url_for("artists.get_artists", page=page-1, **params)

        return paginate_obj.items, pagination


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
