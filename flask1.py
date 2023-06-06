import os
from flask import Flask, render_template, request
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("main.html")

@app.route('/')
def home():
   return template.render(name=request.args.get('name'))


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
