
from app import app
from .forms import PokeForm, LoginForm, RegisterForm
from flask import render_template, request, flash, redirect, url_for
import requests
from .models import User
from flask_login import current_user, logout_user, login_required, login_user


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        email = request.form.get('email').lower()
        password = request.form.get('password')
        u = User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash('Welcome to Fakebook', "success")
            return redirect(url_for('index')) #good login
        flash('Incorrect email password combo', "danager")
        return render_template('login.html.j2', form=form) #bad login
    return render_template('login.html.j2', form=form) #get request

@app.route('/logout')
# @login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out','warning')
        return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
        except:
            flash('There was an unexpected error creating your account. Please try again.', 'danger')
            return render_template('register.html.j2', form=form)
        # if it works
        flash('You have registered successfully', 'success')
        return redirect(url_for('login'))
    # get return
    return render_template('register.html.j2', form=form)

           
#jinja form day2
@app.route('/pokesearch', methods=['GET', 'POST'])
def pokesearch():
    form = PokeForm()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon = request.form.get('pokemon')
        #We will do the login stuff
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
        response = requests.get(url)
        if response.ok:
            pokedex = {
                "sprite": response.json()['sprites']['other']['official-artwork']['front_default'],
                "name":response.json()['forms'][0]['name'],
                "ability_1":response.json()['abilities'][0]['ability']['name'],
                "ability_2":response.json()['abilities'][1]['ability']['name'],
                "ability_3":response.json()['abilities'][2]['ability']['name'],
                "base_xp":response.json()['base_experience'],
                "weight":response.json()['weight'],
                "type":response.json()['types'][0]['type']['name']
                
            }
            return render_template('pokesearch.html.j2', stats = pokedex, form = form)
        else:
            error_string = "Page isn't working. "
            return render_template('pokesearch.html.j2', error = error_string, form = form)
    return render_template('pokesearch.html.j2', form = form)




# pokemon_search('poliwag')

# my_fighters= ['flareon', 'pachirisu', 'jirachi', 'roselia', 'aurorus']