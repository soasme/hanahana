
from datetime import datetime

from hana.core import db


class Hana(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, nullable=False)
    to_id = db.Column(db.Integer, nullable=False)
    is_private = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    remark = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __str__(self):
        return f'{self.from_id} == 🌸 => {self.to_id}'

    def as_dict(self):
        return dict(
            id=self.id,
            from_id=self.from_id,
            to_id=self.to_id,
            remark=self.remark,
            created_at=self.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
            updated_at=self.updated_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
        )
