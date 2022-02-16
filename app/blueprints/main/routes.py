
from .import bp as main
from flask import render_template
from app.models import User
from flask_login import  login_required


@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@main.route('/show_players', methods=['GET', 'POST'])  
@login_required      
def show_players():
    ## Find all our users
    users= User.query.all()
    return render_template('show_players.html.j2', users=users)


