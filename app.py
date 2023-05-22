from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://peixinho:peixinho@codefast.cluster-cjb1qt4dgm8p.us-east-1.rds.amazonaws.com:3306/codefast'
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy()
migrate = Migrate(app, db)
CORS(app)

db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False, nullable=False)
    email = db.Column(db.String(120), index=True, unique=False, nullable=False)

    # relationship field
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

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


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False, nullable=False)
    checked = db.Column(db.Boolean, default=False)
    validation = db.Column(db.String(64), default="Em progresso")
    unplaced = db.Column(db.Boolean, default=False)
    points = db.Column(db.Integer, default=0, nullable=False)
    time = db.Column(db.Integer, default=0)
    users = db.relationship('User', backref='team')

    def __repr__(self):
        return '<Team {}, ID: {}>'.format(self.name, self.id)

    def to_dict(self, fields=None):
        if fields:
            data = {}
            for field in fields:
                if field in self.__dict__.keys():
                    data.update({field: self.__dict__[field]})
        else:
            users_dict = [user.to_dict() for user in self.users]

            data = {
                'id': self.id,
                'name': self.name,
                'checked': self.checked,
                'users': users_dict,
                "validation": self.validation,
                "unplaced": self.unplaced,
                "time": self.time,
                "points": self.points
            }

        return data

    def from_dict(self, data):
        for field in ['id', 'name', 'checked', 'users', 'points', 'time']:
            if field in data:
                setattr(self, field, data[field])


# USERS SERVICE
@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()

    users_dict = [user.to_dict() for user in users]

    return jsonify({'item': users_dict})


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

    return jsonify({'item': user.to_dict()}), 201


# TEAM SERVICE
@app.route('/team', methods=['GET'])
def get_teams():
    teams = Team.query.all()

    teams_dict = [team.to_dict() for team in teams]

    return jsonify({'item': teams_dict})


@app.route('/team/<id>', methods=['GET'])
def get_indidivual_team(id):
    team = Team.query.filter_by(id=id).first()

    return jsonify({'item': team.to_dict()})


@app.route('/team', methods=['POST'])
def create_team():
    data = request.get_json() or {}

    requireds = ['name']
    absent = [field for field in requireds if field not in data]

    if len(absent) > 0:
        raise Exception('Fields requireds')

    team = Team()

    team.from_dict(data)
    db.session.add(team)
    db.session.commit()

    return jsonify({'item': team.to_dict()}), 201


@app.route('/team/<id>', methods=['PUT'])
def edit_team(id):
    data = request.get_json() or {}

    team = Team.query.filter_by(id=id).first()

    if 'name' in data:
        team.name = data['name']
    if 'checked' in data:
        team.checked = data['checked']
    if 'validation' in data:
        team.validation = data['validation']
    if 'points' in data:
        team.points = data['points']
    if 'time' in data:
        team.time = data['time']

    

    
    if 'id_users' in data:
        for id_user in data['id_users']:
            user = User.query.filter_by(id=id_user).first()
            user.team_id = team.id

    db.session.add(team)
    db.session.commit()

    return jsonify({'item': team.to_dict()}), 201
