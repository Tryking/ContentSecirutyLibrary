from app import app
from flask import render_template


@app.route('/dev', methods=['GET', 'POST'])
def index():
    return render_template('index_dev.html')


@app.route('/', methods=['GET', 'POST'])
def index_original():
    return render_template('index.html')


@app.route('/index2')
def index2():
    return render_template('index2.html')
