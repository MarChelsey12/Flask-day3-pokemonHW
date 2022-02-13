from .import bp as battle
from .forms import PokeForm
from flask import render_template, request, flash, redirect, url_for
from app.models import User, Pokemon, PokemonTrainer
from flask_login import current_user, login_required
import requests


@battle.route('/pokesearch', methods=['GET', 'POST'])
@login_required
def pokesearch():
    form = PokeForm()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon = request.form.get('pokemon')
        poke = Pokemon.query.filter_by(name=pokemon).first()
        if poke:
            return render_template('pokesearch.html.j2', poke = poke, form = form)
        else:
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
            response = requests.get(url)
            if response.ok:
                pokedex = {
                    "sprite": response.json()['sprites']['other']['official-artwork']['front_default'],
                    "name":response.json()['forms'][0]['name'],
                    "ability":response.json()['abilities'][0]['ability']['name'],
                    "move":response.json()['moves'][0]['move']['name'],
                    "base_xp":response.json()['base_experience'],
                    "weight":response.json()['weight'],
                    "p_type":response.json()['types'][0]['type']['name']
                }
                new_poke_object = Pokemon()
                new_poke_object.from_dict(pokedex)
                new_poke_object.save()
                poke = Pokemon.query.filter_by(name=pokemon).first()
                return render_template('pokesearch.html.j2', poke = poke, form = form)
            else:
                error_string = "Page isn't working. "
                return render_template('pokesearch.html.j2', error = error_string, form = form)
    return render_template('pokesearch.html.j2', form = form)


@battle.route('/my_pokeballs')
@login_required
def my_pokeballs():
    # get all the pokemon caught for the person using my site
    poke = current_user.pokeballs
    return render_template('my_pokeballs.html.j2', poke = poke)


@battle.route('/training/<int:id>', methods = ['GET', 'POST'])
@login_required
def training(id):
    is_added = Pokemon.query.get(id)
    if len(current_user.pokeballs.all()) == 5:
        flash('Your Pokemon bank is full. Please remove Pokemon before adding.', 'danger')
        return redirect(url_for('battle.pokesearch'))
    elif is_added:
        current_user.catch(is_added)
        flash("You have caught the Pokemon!", "success")
        return redirect(url_for('battle.pokesearch'))
    else:
        flash("Oh no! It escaped or your pokeballs are maxed!", "warning")
        return redirect(url_for('battle.pokesearch'))

    
@battle.route('/release/<int:id>')
@login_required
def release(id):
    is_freed = Pokemon.query.get(id)
    current_user.free(is_freed)
    flash(f"You have freed the Pokemon.", "success")
    return redirect(url_for('battle.pokesearch'))
