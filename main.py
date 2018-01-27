from flask import Flask, render_template, session, request
from utils import dbhelper as db

#Send noots
app = Flask(__name__)

@app.route("/")
def mainpage():
    return render_template("index.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        uname = request.args.get("username")
        hashpw = hash(request.args.get("password"))
        return db.checkLogin(uname, hashpw)

@app.route("/signup")
def signup():
    return "hi"


@app.route("/showaccounts")
def accounts():
    return str(db.viewAccounts())

if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0")