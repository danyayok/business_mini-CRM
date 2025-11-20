from sqlalchemy.orm import Session

class BaseRepo:
    def __init__(self, db: Session):
        self.db = db

    def get(self, model, id: int):
        return self.db.query(model).filter(model.id == id).first()

    def create(self, model, data: dict):
        obj = model(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj, data: dict):
        for field, value in data.items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj):
        self.db.delete(obj)
        self.db.commit()