from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    update_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    ideas = db.relationship("Idea", backref='user', lazy=True)

    def __str__(self):
        return self.name


class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(250), nullable=False)
    type = db.Column(db.String(250), nullable=False)
    participants = db.Column(db.Integer)
    price = db.Column(db.Float)
    link = db.Column(db.String(250))
    key = db.Column(db.Integer, nullable=False)
    accessibility = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))