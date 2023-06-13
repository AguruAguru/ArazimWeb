import os
import random

import flask
from flask import Flask, render_template, request
import json
import base64
import ast

app = Flask(__name__)

@app.route('/')
def index():
    info = request.cookies.get('info')
    return render_template("index.html", info="" if info is None else "Hello " + info + "!")

@app.route('/login')
def login():
    resp = resp = flask.make_response(render_template("login.html"))
    name = request.args.get("name")
    if name is not None:
        name = "user_" + name
    psw = request.args.get("psw")
    err = None
    if None not in [name, psw]:
        resp = flask.redirect(flask.url_for('index'))
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
    if name is not None:
        name = "user_" + name
    psw = request.args.get("psw")
    if None not in [name, psw]:
        with open('data.json', 'r+') as f:
            data = json.load(f)
            if len(psw) < 4:
                err = "Password too small"
            if name in data:
                err = "Name taken"
            if name == "user_":
                err = "name cant be empty"
            if err is None:
                data[name] = psw
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        return flask.redirect(flask.url_for('index'))
    return render_template('signup.html', err="" if err is None else err)


@app.route('/feed', methods=['GET', 'POST'])
def feed():

    info = request.cookies.get('info')
    logged_in = info is not None
    if not logged_in:
        return flask.redirect(flask.url_for('index'))
    elif request.method == 'POST' and request.form['submit'] == "Submit":
        print("a")
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            print("b")
            filename = "".join([chr(random.randint(ord('a'),ord('z'))) for i in range(20)]) + ".jpg"
            uploaded_file.save(os.path.join("static", filename))
            with open('data.json', 'r+') as f:
                data = json.load(f)
                key = info + "_gallery"
                if key not in data:
                    data[key] = ""
                gallery = data[key].split("\0")
                gallery.append(filename)
                data[key] = "\0".join(gallery)
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()

    with open('data.json', 'r') as f:
        data = json.load(f)
        i = 0
        feed = []
        for key in data.keys():
            if len(feed) >= 4:
                break
            if "user_" in key and key[5:]+"_gallery" in data:
                feed += [(img,key[5:]+"_gallery") for img in data[key[5:]+"_gallery"].split("\0")]
                if ("",key[5:]+"_gallery") in feed:
                    feed.remove(("",key[5:]+"_gallery"))
    urls, users = [], []
    for img, user in feed:
        if i >= 4:
            break
        urls.append(flask.url_for('static', filename=img))
        users.append(user)
        i += 1
    return render_template('feed.html', feed=urls, users=users)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)

"""
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <a href = "/">Back</a>
    <div>
      <button type="sybmit" name="upload" value="pressed">Upload</button>
    </div>
</body>

"""