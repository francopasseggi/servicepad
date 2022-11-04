from servicepad.extensions import db
from sqlalchemy.sql import func


class Publication(db.Model):
    """Publication model"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f'Publication {self.title} by {self.user_id}'
