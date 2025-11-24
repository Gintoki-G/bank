from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = "test"

USERS = {
    "admin@naver.com": {"password": "123400", "balance": 500000, "name" : "김예나"}
}

#flask의 기본구조
#1. @app.route()    → URL 등록
#2. 함수            → 실행할 코드
#3. return          → HTML or redirect

@app.route('/',methods=['GET', 'POST'])
def login() :
    if request.method == "POST" :
        useremail = request.form['email']
        password = request.form['password']

        user = USERS.get(useremail)
        #user = {"password": "1234", "balance": 500000}
        #if True and user["password"] == password:

        if  user and user["password"] == password :
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
        if password == password2 : 
            if useremail in USERS :
                return "이미 회원가입이 되어있습니다"
            else : 
                USERS[useremail] = {
                "password": password,
                "balance" : 50000,
                "name" : name
                }
                return redirect(url_for("login"))
        else : 
            return "비밀번호가 다릅니다."
    return render_template("newAccount.html")

@app.route('/dashboard')
def dashboard():
    return "대시보드 준비중!"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)