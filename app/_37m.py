from app import db
from datetime import datetime

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page=1, per_page=10, endpoint='', **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'data': [item.to_dict() for item in resources.items]
        }
        data['meta'] = {
            'page': page,
            'total_pages': resources.pages,
            'total_items': resources.total
        }
        if query.count() < 1:
            data['data'] = []
        if endpoint != '':
            data['_links'] = {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, 
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        return data

class Text(PaginatedAPIMixin, db.Model):
    time = db.Column(db.DateTime, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Unicode(37))

    def __init__(self, body):
        self.body = body
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        data = {
            'id': self.id,
            'time': self.time,
            'body': self.body
        }
        return data

    @staticmethod
    def search(q, page, per_page):
        if '*' in q or '_' in q:
            _q = q.replace('_', '__')\
                .replace('*', '%')\
                .replace('?', '_')
        else:
            _q = '%{0}%'.format(q)
        r = Text.query.filter(Text.body.ilike(_q)).order_by(Text.time.desc())
        return Text.to_collection_dict(r, page, per_page)