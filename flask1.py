import os
from flask import Flask, render_template, request
import json


app = Flask(__name__)


@app.route('/signup')
def homepage():
    err = None
    name = request.args.get("name")
    psw = request.args.get("psw")
    if None not in [name, psw]:
        with open('data.json', 'r+') as f:
            data = json.load(f)
            if len(psw) < 4:
                err = "Password too small"
            if name in data:
                err = "Name taken"
            if name == "":
                err = "name cant be empty"
            if err is None:
                data[name] = psw
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=4)
            f.truncate()
    return render_template('main.html', err="" if err is None else err)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
