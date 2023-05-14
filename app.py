from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mysqldb import MySQL


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:734946@localhost/codefast'


db = SQLAlchemy()
migrate = Migrate()
mysql = MySQL()

db.init_app(app)


class User(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False, nullable=False)
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

    

@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()
    
    users_dict = [user.to_dict() for user in users]

    return jsonify(users_dict)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}

    requireds = ['name', 'email']
    absent = [field for field in requireds if field not in data]

    if len(absent) > 0:
        raise Exception('Fields requireds')
    
    user = User()

    user.from_dict(data)
    db.session.add(user)
    db.session.commit()

    return jsonify({'oret': user.to_dict()}), 201

    

