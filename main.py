from flask import Flask, render_template, session, request, redirect
from utils import dbhelper as db
import bcrypt

#Send noots
app = Flask(__name__)
db.getCursorFromFile("data/data.db")

@app.route("/")
def mainpage():
    if not "username" in session.keys():
        return render_template("index.html")
    else:
        return redirect("/home")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        if not "username" in session.keys():
            uname = request.form["username"]
            pw = request.form["password"]
            print("Username requested:", uname, "Passhash:", pw)
            pwhash =  db.getPWHash(uname)
            success =  pwhash is not None and bcrypt.hashpw(pw.encode("UTF-8"), pwhash) == pwhash
            if success:
                session["username"] = uname
                return redirect("/home")
            else:
                return redirect("/login")
        else:
            return redirect("/home")

@app.route("/edit/<paper_id>")
def edit(paper_id):
    return render_template("essay.html", essay = db.getEssay(paper_id))

@app.route("/home")
def home():
    return render_template("index2.html")

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    elif request.method == 'POST':
        uname = request.form["username"]
        hashpw = bcrypt.hashpw(request.form["password"].encode("UTF-8"), bcrypt.gensalt())
        if db.nameAvailable(uname):
            db.execQuery("INSERT INTO ACCOUNTS VALUES (?, ?, ?, ?)", (db.getNewId("ACCOUNTS"), uname, hashpw, 0))
            return redirect("/login")
        else:
            return redirect("/signup")

@app.route("/upload", methods = ["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    elif request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        db.execQuery("INSERT INTO PAPERS VALUES (?, ?, ?, ?)", (db.getNewId("PAPERS"), db.getUserID(session["username"]), title, content))
        return redirect("/activity")

@app.route("/activity")
def activity():
    return render_template("activity.html")


@app.route("/showaccounts")
def accounts():
    return str(db.viewAccounts())

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "hello dog"
    app.run(host = "0.0.0.0")