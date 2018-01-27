from flask import Flask, render_template, session, request, redirect
from utils import dbhelper as db
import bcrypt

#Send noots
app = Flask(__name__)
db.getCursorFromFile("data/data.db")

@app.route("/")
def mainpage():
    return render_template("index.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        uname = request.form["username"]
        pw = request.form["password"]
        print("Username requested:", uname, "Passhash:", pw)
        return db.getPWHash(uname)



@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    elif request.method == 'POST':
        uname = request.form["username"]
        hashpw = bcrypt.hashpw(request.form["password"], bcrypt.gensalt())
        if db.nameAvailable(uname):
            db.execQuery("INSERT INTO ACCOUNTS VALUES (?, ?, ?, ?)", (db.getNewId("ACCOUNTS"), uname, hashpw, 0))
            return redirect("/login")
        else:
            return redirect("/signup")

@app.route("/upload", methods = ["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")

@app.route("/showaccounts")
def accounts():
    return str(db.viewAccounts())

if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0")