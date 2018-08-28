from jinja2 import TemplateNotFound

from app import app
from flask import render_template, url_for, make_response, redirect, request


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index_dev.html')


@app.route('/index')
def index1():
    return render_template('index.html')


@app.route('/index2')
def index2():
    return render_template('index2.html')


@app.route('/pages/charts/<item>')
def pages_charts(item):
    return to_template(item)


@app.route('/pages/forms/<item>')
def pages_forms(item):
    return to_template(item)


@app.route('/pages/layout/<item>')
def pages_layout(item):
    return to_template(item)


@app.route('/pages/mailbox/<item>')
def pages_mailbox(item):
    return to_template(item)


@app.route('/pages/tables/<item>')
def pages_tables(item):
    return to_template(item)


@app.route('/pages/UI/<item>')
def pages_UI(item):
    return to_template(item)


@app.route('/pages/examples/<item>')
def pages_examples(item):
    return to_template(item)


def to_template(item):
    path = request.path.strip('/')
    template = path
    if 'html' not in item:
        template = template + '.html'
    return render_template(template)


@app.errorhandler(404)
def page_not_found(error):
    # 找不到的页面定向到404
    resp = make_response(render_template('pages/examples/404.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


@app.errorhandler(TemplateNotFound)
def page_not_found(error):
    # 资源找不到也定向到404页面
    resp = make_response(render_template('pages/examples/404.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp
