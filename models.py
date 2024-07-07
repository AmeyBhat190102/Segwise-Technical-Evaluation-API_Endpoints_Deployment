from app import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appid = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    release_date = db.Column(db.String)
    required_age = db.Column(db.Integer)
    price = db.Column(db.Float)
    dlc_count = db.Column(db.Integer)
    about_the_game = db.Column(db.Text)
    supported_languages = db.Column(db.String)
    windows = db.Column(db.Boolean)
    mac = db.Column(db.Boolean)
    linux = db.Column(db.Boolean)
    positive = db.Column(db.Integer)
    negative = db.Column(db.Integer)
    score_rank = db.Column(db.Integer)
    developers = db.Column(db.String)
    publishers = db.Column(db.String)
    categories = db.Column(db.String)
    genres = db.Column(db.String)
    tags = db.Column(db.String)


db.create_all()
