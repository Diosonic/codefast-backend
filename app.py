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




team_has_seed = db.Table('team_has_seed',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True),
    db.Column('seed_id', db.Integer, db.ForeignKey('seed.id'), primary_key=True),
)

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

    # relationship fields
    # seed_id = db.Column(db.Integer, db.ForeignKey('seed.id'))

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
            data = {
                'id': self.id,
                # 'seed_id': self.seed_id,
                'name': self.name,
                'checked': self.checked,
                'users': [user.to_dict() for user in self.users],
                "validation": self.validation,
                "unplaced": self.unplaced,
                "time": self.time,
                "points": self.points
            }

        return data

    def from_dict(self, data):
        for field in ['id', 'name', 'checked', 'users', 'points', 'time', 'seed_id']:
            if field in data:
                setattr(self, field, data[field])


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))

    seeds = db.relationship('Seed', backref='Round')

    def __repr__(self):
        return '<Round {}, ID: {}>'.format(self.title, self.id)

    def to_dict(self, fields=None):
        if fields:
            data = {}
            for field in fields:
                if field in self.__dict__.keys():
                    data.update({field: self.__dict__[field]})
        else:

            data = {
                'id': self.id,
                'title': self.title,
                'seeds': [seed.to_dict() for seed in self.seeds],
            }

        return data

    def from_dict(self, data):
        for field in ['id', 'title']:
            if field in data:
                setattr(self, field, data[field])


class Seed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_match = db.Column(db.DateTime)

    # relationship fields
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'))

    # teams = db.relationship('Team', backref='seed')
    teams = db.relationship('Team', secondary=team_has_seed, backref='teams')

    def __repr__(self):
        return '<Seed {}, ID: {}>'.format(self.date_match, self.id)

    def to_dict(self, fields=None):
        if fields:
            data = {}
            for field in fields:
                if field in self.__dict__.keys():
                    data.update({field: self.__dict__[field]})
        else:
            data = {
                'id': self.id,
                'round_id': self.round_id,
                'date_match': self.date_match,
                'teams': [team.to_dict() for team in self.teams],
            }

        return data

    def from_dict(self, data):
        for field in ['id', 'date_match', 'round_id']:
            if field in data:
                setattr(self, field, data[field])


class ClassificationScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    in_progress = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Round ID: {}>'.format(self.id)

    def to_dict(self, fields=None):
        if fields:
            data = {}
            for field in fields:
                if field in self.__dict__.keys():
                    data.update({field: self.__dict__[field]})
        else:

            data = {
                'id': self.id,
                'in_progress': self.in_progress,
            }

        return data

    def from_dict(self, data):
        for field in ['id', 'in_progress']:
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
    teams = Team.query.order_by(Team.points.desc()).all()

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
    if 'seed_id' in data:
        team.seed_id = data['seed_id']
    if 'unplaced' in data:
        team.unplaced = data['unplaced']

    if 'id_users' in data:
        for id_user in data['id_users']:
            user = User.query.filter_by(id=id_user).first()
            user.team_id = team.id

    db.session.add(team)
    db.session.commit()

    return jsonify({'item': team.to_dict()}), 201


# ROUND SERVICE
@app.route('/rounds', methods=['GET'])
def get_rounds():

    rounds = Round.query.all()

    rounds_dict = [round.to_dict() for round in rounds]

    return jsonify({'item': rounds_dict})


@app.route('/rounds/<id>', methods=['GET'])
def get_round(id):

    rounds = Round.query.filter_by(id=id).first()

    return jsonify({'item': rounds.to_dict()})


@app.route('/rounds', methods=['POST'])
def create_round():
    data = request.get_json() or {}

    requireds = ['title']
    absent = [field for field in requireds if field not in data]

    if len(absent) > 0:
        raise Exception('Fields requireds')

    rounds = Round()

    rounds.from_dict(data)
    db.session.add(rounds)
    db.session.commit()

    return jsonify({'item': rounds.to_dict()}), 201


# SEEDS SERVICE
@app.route('/seeds', methods=['GET'])
def get_seeds():

    seeds = Seed.query.all()

    seeds_dict = [seed.to_dict() for seed in seeds]

    return jsonify({'item': seeds_dict})


@app.route('/seeds/round/<round_id>', methods=['GET'])
def get_seed(round_id):

    seeds = Seed.query.filter_by(round_id=round_id).all()
    seeds_dict = [seed.to_dict() for seed in seeds]
    return jsonify({'item': seeds_dict})


@app.route('/seeds', methods=['POST'])
def create_seed():
    data = request.get_json() or {}

    seeds = Seed()

    seeds.from_dict(data)
    db.session.add(seeds)
    db.session.commit()

    return jsonify({'item': seeds.to_dict()}), 201


@app.route('/seeds/team', methods=['POST'])
def create_seeds_has_team():
    data = request.get_json()

    seed_id = data.get('seed_id')
    team_id = data.get('team_id')

    seed = Seed.query.get(seed_id)
    team = Team.query.get(team_id)

    if not seed or not team:
        return jsonify({'message': 'Livro ou autor não encontrado'}), 404

    seed.teams.append(team)
    db.session.commit()

    return jsonify({'item': seed.to_dict()}), 201


# CLASSIFICATION SCORE SERVICE
@app.route('/classification/progress', methods=['GET'])
def get_progress():
    
    classification_score = ClassificationScore.query.first()

    return jsonify({'item': classification_score.to_dict()})


@app.route('/classification/<id>', methods=['PUT'])
def change_progress(id):
    data = request.get_json() or {}

    classification = ClassificationScore.query.filter_by(id=id).first()

    if 'in_progress' in data:
        classification.in_progress = data['in_progress']

    db.session.add(classification)
    db.session.commit()

    return jsonify({'item': classification.to_dict()}), 201