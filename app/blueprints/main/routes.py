
from .import bp as main
from flask import render_template


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')
           
def show_users():
    ## Find all our users
    users=User.query.all()
    return render_template('show_users.html.j2', users=users)
