import flask
import random
import json
import os

app = flask.Flask(__name__)
_id = random.random()*9999


def o():
    a = open(f"log-{_id}", "w")
    a.write("")
    a.close()


o()


@app.route("/", methods=["POST"])
def root():
    global _id
    if not os.path.exists(f"log-{_id}"):
        o()
    if flask.request.data:
        d = json.loads(flask.request.data)
        if 'clear' in dict(d).keys():
            if d['clear']:
                _id = random.random()*9999
                o()
        f = open(f"log-{_id}", "a")
        f.write(f"{json.dumps(d)}\n")
        f.close()
        return {"Resp": "sucess"}, 200
    else:
        f = open(f"log-{_id}", "r")
        lines = f.read().split("\n")
        data = []
        for l in lines:
            if l == "":
                continue
            data.append(json.loads(l))
        return {"data": data}


app.run("0.0.0.0", 8601, debug=True)
