import os
from flask import Flask
from flask import render_template, request, url_for, redirect, session
from models import db, cuser
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm

app = Flask(__name__)

@app.route('/')
def home():
    Username = session.get('username', None)
    Userid = session.get('userid', None)
    return render_template("main.html", name = Username, id = Userid)

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
        session['userid'] = form.data.get('userid')  # 세션  userid와 폼의 userid가 같은지 검사
        Luser = session.get('userid', None)
        print("Login")
        print("User name: %s " %Luser)
        return redirect('/')  # 로그인에 성공하면 홈화면으로 redirect
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid',None)
    return redirect(url_for('home'))

@app.route('/find_password')
def find():
    return '안녕'

if __name__ == "__main__":
    BASE_DIR = os.path.abspath(__file__)    #DB 경로를 상대 경로로 설정
    DIR = os.path.join(BASE_DIR, "DB")
    FILE = 'DB/db.sqlite'
    TARGET_FILE_FULL_PATH = os.path.join(DIR, FILE)             #DB file 만들기

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + FILE
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = 'rkdtlsgml40'
    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)
    db.app = app
    db.create_all()

    app.run(debug=True, host='127.0.0.1', port='5000')