from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class cuser(db.Model):
    __table_name__ = 'user'                           #테이블 이름 : user
    id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
    password = db.Column(db.String(64), unique = True, nullable = False)
    userid = db.Column(db.String(32), unique = True, nullable = False)
    username = db.Column(db.String(8), unique = True, nullable = False)
    email = db.Column(db.String(32), nullable = False)
    profile_image = db.Column(db.String(100), default='default.png')
