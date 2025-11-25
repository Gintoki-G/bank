from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite3'

db = SQLAlchemy(app)

# =========================
# 모델 정의
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    balance = db.Column(db.Integer, default=50000)

# =========================
# 라우트
# =========================
@app.route('/create')
def create():
    db.create_all()
    return "DB 생성 완료"

@app.route('/add')
def add():
    test_user = User(email="test@example.com", password="1234", name="테스트")
    db.session.add(test_user)
    db.session.commit()
    return "테스트 유저 추가 완료!"
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

#class User(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    email = db.Column(db.String(120), unique=True)
#    password = db.Column(db.String(100))
#    name = db.Column(db.String(100))
#    balance = db.Column(db.Integer, default=50000)


@app.route('/dashboard')
def dashboard():
    if 'useremail' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session['useremail']).first()

    if not user:
        return redirect(url_for('login'))

    return render_template(
        "dashboard.html",
        user=user,                 # 핵심!
        transactions=[]            # 혹시 없으면 빈 리스트라도 넘김
    )

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    # 로그인 사용자 확인
    user = User.query.filter_by(email=session.get('useremail')).first()
    if not user:
        return redirect(url_for('login'))

    if request.method == "POST":
        toemail = request.form['to']
        amount = int(request.form['amount'])  # 숫자로 변환

        # 1) 자기 자신에게 송금 불가
        if toemail == user.email:
            return "자기 자신에게는 송금할 수 없습니다."

        # 2) 받는 사람 검색
        receiver = User.query.filter_by(email=toemail).first()

        if not receiver:
            return "받는 사람이 존재하지 않습니다."

        # 3) 잔액 부족 확인
        if user.balance < amount:
            return "잔액이 부족합니다."

        # 4) 송금 처리
        user.balance -= amount
        receiver.balance += amount
        db.session.commit()

        return redirect(url_for("dashboard"))

    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)