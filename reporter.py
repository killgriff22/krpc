import flask
import random
import json

app = flask.Flask(__name__)
_id = random.random()*9999
a = open(f"log-{_id}", "w")
a.write("")
a.close()


@app.route("/", methods=["POST"])
def root():
    print(flask.request.get_data())
    if flask.request.data:
        d = json.loads(flask.request.data)
        f = open(f"log-{_id}", "a")
        f.write(f"{json.dumps(d)}\n")
        f.close()
        return {"Resp": "sucess"}, 200
    else:
        f = open(f"log-{_id}", "r")
        lines = f.read().split("\n")
        data = []
        for l in lines:
            print(l)
            if l == "":
                continue
            data.append(json.loads(l))
        return {"data": data}


app.run("0.0.0.0", 8601, debug=True)
