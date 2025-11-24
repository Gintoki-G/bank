from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = "test"

USERS = {
    "admin": {"password": "1234", "balance": 500000}
}

#flask의 기본구조
#1. @app.route()    → URL 등록
#2. 함수            → 실행할 코드
#3. return          → HTML or redirect
