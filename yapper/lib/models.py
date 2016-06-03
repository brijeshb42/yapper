from datetime import datetime

from yapper import db
from vomitter import LOGGER as L
from .cache import cache
from .decorators import profile


class BaseModel(db.Model):
    """A base model that is inherited by all the other models.
    It has common columns required by the models."""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow,
                            onupdate=datetime.utcnow)

    @classmethod
    @profile
    def get(cls, mid):
        L.d('Getting from Cache.')
        obj = cache.get(cls.key(mid))
        if obj:
            L.d('Cache hit for - %s' % cls.key(mid))
            return obj
        L.d('Cache miss for - %s' % cls.key(mid))
        obj = cls.query.get(mid)
        if obj:
            L.d('Saving in cache - %s' % cls.key(mid))
            cache.set(cls.key(mid), obj)
        else:
            L.d('The object was None')
        return obj

    def to_json(self):
        return {'id': self.id}

    def save(self):
        db.session.add(self)
        db.session.commit()
        cache.set(self.key(self.id), self)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        cache.delete(self.key(self.id))

    @classmethod
    def key(cls, mid):
        return ':model_key:%s:%s' % (cls.__tablename__, str(mid))

    @classmethod
    def save_all(cls, items):
        db.session.add_all(items)
        db.session.commit()
