import os

import flask
from flask import Flask, render_template, request
import json


app = Flask(__name__)

@app.route('/')
def index():
    info = request.cookies.get('info')
    return render_template("index.html", info="" if info is None else "Hello " + info + "!")

@app.route('/login')
def login():
    resp = flask.make_response(render_template("login.html"))
    name = request.args.get("name")
    psw = request.args.get("psw")
    err = None
    if None not in [name, psw]:
        with open('data.json', 'r+') as f:
            data = json.load(f)
            if name in data.keys() and data[name]==psw:
                resp.set_cookie('info', request.args.get("name"))
            else:
                err = "incorrect details"
    if err is not None:
        resp = flask.make_response(render_template("login.html", err=err))
    return resp


@app.route('/signup')
def signup():
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
    return render_template('signup.html', err="" if err is None else err)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
