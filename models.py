from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#SQLAlchemy를 사용해 데이터베이스 저장

class cuser(db.Model):
    __table_name__ = 'user'                           #테이블 이름 : user
    id = db.Column(db.Integer, primary_key = True, nullable = False)   #id를 기본키로 설정
    password = db.Column(db.String(64), nullable = False)              #패스워드를 받아올 문자열길이
    userid = db.Column(db.String(32), nullable = False)                #이하 위와 동일
    username = db.Column(db.String(8), nullable = False)
    email = db.Column(db.String(32), nullable = False)
    check = db.Column(db.String(8), nullable = False)
    profile_image = db.Column(db.String(100), default='default.png')
