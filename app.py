from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "test"
#데이터 베이스 연결 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# SQLite 사용 예시
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite3'

db = SQLAlchemy(app)

@app.route('/create')
def create():
    db.create_all()
    return "DB 생성 완료"

@app.route('/add')
@app.route('/add')
def add():
    # 테스트용 유저 추가
    test_user = User(
        email="test@example.com",
        password="1234",
        name="테스트",
        balance=50000
    )
    # DB에 추가
    db.session.add(test_user)
    db.session.commit()
    return "테스트 유저 추가 완료!"

#데이터 베이스 연결 완료
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    balance = db.Column(db.Integer, default=50000)
#flask의 기본구조
#1. @app.route()    → URL 등록
#2. 함수            → 실행할 코드
#3. return          → HTML or redirect

@app.route('/',methods=['GET', 'POST'])
def login() :
    if request.method == "POST" :
        useremail = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=useremail).first()
        #user = {"password": "1234", "balance": 500000}
        #if True and user["password"] == password:

        if  user and user.password == password :
            session['useremail'] = useremail
            return redirect(url_for("dashboard"))
        else :
            return "로그인 실패"
    return render_template("login.html")

@app.route('/newAccount',methods=['GET','POST'])
def newAccount():
    if request.method == "POST":
        useremail = request.form['email']
        password = request.form['password']
        password2 = request.form['pw2']
        name = request.form['name']

        if password != password2:
            return "비밀번호가 다릅니다."

        # 기존 유저 검사 (DB에서 조회)
        exist = User.query.filter_by(email=useremail).first()
        if exist:
            return "이미 회원가입이 되어있습니다."

        # 새 유저 DB 저장
        new_user = User(email=useremail, password=password, name=name)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("newAccount.html")


@app.route('/dashboard')
def dashboard():
    return "대시보드 준비중!"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)