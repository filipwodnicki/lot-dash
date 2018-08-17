from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.name)