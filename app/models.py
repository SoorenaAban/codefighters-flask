import datetime
from . import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    reports = db.relationship('Report', backref='reported_player', lazy='dynamic')
    reports_made = db.relationship('Report', backref='reporting_player', lazy='dynamic')

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    player_one_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    player_two_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('players.id'))

class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    reported_player = db.relationship('Player', backref='reports', lazy='dynamic')
    reporting_player = db.relationship('Player', backref='reports_made', lazy='dynamic')
    reason = db.Column(db.String(64))
    description = db.Column(db.String(256))

class MessageType:
    USERMESSAGE = 0
    NOTIFICATION = 1

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    type = db.Column(db.Integer)

class GameLogType:
    ACTION = 0
    ERROR = 1
    INFO = 2

class GameLog(db.Model):
    __tablename__ = 'gamelogs'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    log_body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    type = db.Column(db.Integer)

