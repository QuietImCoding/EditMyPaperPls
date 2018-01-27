from flask import Flask, render_template
from utils import dbhelper as db

#Send noots
app = Flask(__name__)

@app.route("/")
def mainpage():
    return render_template("homepage.html")
    # id = db.getNewId("ACCOUNTS")
    # db.execQuery("INSERT INTO ACCOUNTS VALUES (?,?,?,?)", (id, "dog" + str(id), "AAAA", 0))
    # return str(db.getNewId("ACCOUNTS"))

@app.route("/showaccounts")
def accounts():
    return str(db.viewAccounts())

if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0")