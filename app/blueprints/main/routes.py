
from .import bp as main
from flask import render_template



@main.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')
           