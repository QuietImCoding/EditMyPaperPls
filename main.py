from flask import Flask

#Send noots
app = Flask(__name__)

@app.route("/")
def mainpage():
    return "sup dood"

if __name__ == "__main__":
    app.run(host = "0.0.0.0")