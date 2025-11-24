from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = "test"

USERS = {
    "admin@naver.com": {"password": "123400", "balance": 500000}
}

#flask의 기본구조
#1. @app.route()    → URL 등록
#2. 함수            → 실행할 코드
#3. return          → HTML or redirect

@app.route('/',methods=['GET', 'POST'])
def login() :
    if request.method == "Post" :
        useremail = request.form['email']
        password = request.form['password']

        user = USERS.get('useremail')
        #user = {"password": "1234", "balance": 500000}
        #if True and user["password"] == password:

        if  user and user["password"] == password :
            session['useremail'] = useremail
            return redirect(url_for("dashboard"))
        else :
            return "로그인 실패"
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)