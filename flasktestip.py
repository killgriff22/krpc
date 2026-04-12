import flask
app = flask.Flask(__name__)

@app.route("/")
def r():
    return " "

app.run("0.0.0.0",8080)