from app import db
from uuid import uuid4

def gen_uuid():
    return str(uuid4())

class ModelMixin:
    def save(self, commit=True):
        # Save this model to the database.
        db.session.add(self)
        if commit:
            db.session.commit()
        return self
