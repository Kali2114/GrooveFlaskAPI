"""
Models in databse.
"""

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