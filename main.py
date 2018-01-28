from flask import Flask, render_template, session, request, redirect, json
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
            pwhash =  db.getPWHash(uname)
            success =  pwhash is not None and bcrypt.hashpw(pw.encode("UTF-8"), pwhash) == pwhash
            if success:
                session["username"] = uname
                return redirect("/home")
            else:
                return redirect("/login")
        else:
            return redirect("/home")

@app.route("/essay/<paper_id>")
def showessay(paper_id):
    edits = db.getEditsForPaper(paper_id)
    print(edits)
    return render_template("essay.html", essay = db.getEssay(paper_id), edits = db.getEditsForPaper(paper_id))

@app.route("/edit")
def edit():
    return render_template("edit.html", allessays = db.getEsssayList())

@app.route("/myessays")
def myessays():
    return render_template("myessays.html", myessays = db.getEssaysByUser(session["username"]))

@app.route("/home")
def home():
    return render_template("index2.html", mypoints = db.getPointsForUser(session["username"]), numessays = len(db.getEssaysByUser(session["username"])))

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
        newId = db.getNewId("PAPERS")
        db.execQuery("INSERT INTO PAPERS VALUES (?, ?, ?, ?)", (newId, db.getUserID(session["username"]), title, content))
        return redirect("/activity")

@app.route("/activity")
def activity():
    return render_template("activity.html")

@app.route("/logoff")
def logoff():
    session.pop("username")
    return redirect("/")

@app.route("/addcomments", methods = ["POST"])
def addcomments():
    data = json.loads(request.form["data"])
    for comment in data:
        db.execQuery("INSERT INTO EDITS VALUES (?, ?, ?, ?, ?, ?)",
                     (db.getNewId("EDITS"), comment["start"], comment["end"], db.getUserID(session["username"]), comment["content"], comment["page"]))
    return(str(data))

@app.route("/showaccounts")
def accounts():
    return str(db.viewAccounts())

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "hello dog"
    app.run(host = "0.0.0.0")