import os
from flask import Flask, render_template, request, url_for, redirect, session
from models import db, cuser
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm

app = Flask(__name__)

@app.route('/')
def home():
    Userid = session.get('userid', None)
    return render_template("main.html", id = Userid)
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit(): #유효성검사
        newuser = cuser()
        newuser.userid = form.data.get('userid')
        newuser.username = form.data.get('username')
        newuser.password = form.data.get('password')
        newuser.email = form.data.get('email')
        newuser.check = form.data.get('gender')

        print('New user: %s' %newuser.userid)
        print('Password: %s\n' %newuser.password)
        db.session.add(newuser)
        db.session.commit()

        return redirect(url_for('home'))
    # if request.method == 'GET':
    #     return render_template('register2.html')
    # else:
    #     userid = request.form.get('userid')
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     email = request.form.get('email')
    #     check = request.form.get('gender')
    #     if not (userid and username and password and email and check):
    #         return "모든 항목을 입력해주세요"
    #     else:
    #         user = cuser()
    #         user.password = password
    #         user.userid = userid
    #         user.username = username
    #         user.email = email
    #         user.check = check
    #         db.session.add(user)
    #         db.session.commit()
    #         print('New user: %s' %user.userid)
    #         print('Password: %s\n' %password)
    # return redirect(url_for('home'))

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

    app.run(debug=True, host='127.0.0.2', port='5000')