import os
from flask import Flask, render_template, request, url_for, redirect, session
from models import db, cuser
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm

app = Flask(__name__)

@app.route('/register', methods=['GET, POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        userid = request.form.get('userid')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        if not (userid and username and password and email):
            return "모든 항목을 입력해주세요"
        else:
            user = cuser()
            user.password = password
            user.userid = userid
            user.username = username
            user.email = email
            db.session.add(user)
            db.session.commit()
            print('New user: %s' %user.userid)
            print('Password: %s\n' %password)
    return redirect(url_for('home'))

@app.route('/')
def home():
    Username = session.get('username', None)
    return render_template("main.html", username = Username)

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

    app.run(debug=True, host='10.156.146.101', port='5000')