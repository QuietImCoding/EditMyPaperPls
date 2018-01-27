from flask import Flask

#Send noots
app = Flask(__name__)

@app.route("/")
def mainpage():
    return "sup dood"

if __name__ == "main":
    app.run()