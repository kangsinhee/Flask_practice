import os
from flask import Flask
from flask import render_template, request, url_for, redirect, session, Blueprint
from models import db, cuser
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm, findpassword

app = Flask(__name__)

@app.route('/')
def home():
    Userid = session.get('userid', None)
    username = session.get('username')
    return render_template("main.html", id = Userid, name = username)

@app.route('/register', methods=['GET','POST'])
def register():  # get 요청 단순히 페이지 표시 post요청 회원가입-등록을 눌렀을때 정보 가져오는것
    form = RegisterForm()
    if form.validate_on_submit():  # POST검사의 유효성검사
        user = cuser()  # models.py에 있는 Fcuser
        user.userid = form.data.get('userid')
        user.username = form.data.get('username')
        user.password = form.data.get('password')
        user.email = form.data.get('email')

        print(user.userid, user.password)
        db.session.add(user)
        db.session.commit()
        return "가입 완료"
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # 유효성 검사
        session['userid'] = form.data.get('userid')  #session에 form에서 받아온 id 값 저장
        userid = session.get('userid', None) #userid에 session의 userid 값 저장
        print("Login")
        print("User ID: %s " %userid)

        return redirect('/')  # 로그인에 성공하면 홈화면으로 redirec
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    user = session.get('userid', None)
    print("Logout: %s" %user)
    session.pop('userid',None)
    return redirect(url_for('home'))

@app.route('/find')
def find():
    form = findpassword()
    if form.validate_on_submit():
        return 0
    return render_template('find.html', form=form)

if __name__ == "__main__":
    BASE_DIR = os.path.abspath(__file__)    #DB 경로를 상대 경로로 설정
    DIR = os.path.join(BASE_DIR, "DB")
    FILE = 'DB/db.sqlite'
    TARGET_FILE_FULL_PATH = os.path.join(DIR, FILE)             #DB file 만들기

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + FILE
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #요청의 끝마다 커밋을 함
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #수정사항에 대한 track ㄴ True면 메시지 남

    app.config['SECRET_KEY'] = 'qweasdzxc123'
    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)
    db.app = app
    db.create_all()

    app.run(debug=True, host='127.0.0.1', port='5000')