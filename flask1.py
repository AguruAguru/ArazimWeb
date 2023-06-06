import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
@app.route('/')
def home():
   return render_template('main.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
