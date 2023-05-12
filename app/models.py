from app import db

class User(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
  
    def __repr__(self):
        return '<User {}, ID: {}>'.format(self.name, self.id)
    
    def to_dict(self, fields=None):
        if fields:
            data = {}
            for field in fields:
                if field in self.__dict__.keys():
                    data.update({field: self.__dict__[field]})
        else:
            data = {
                'id': self.id,
                'name': self.name,
                'email': self.email
            }

        return data
    
    def from_dict(self, data):
        for field in ['id', 'name', 'email']:
            if field in data:
                setattr(self, field, data[field])