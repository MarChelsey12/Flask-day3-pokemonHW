from .import bp as bat
from .forms import PokeForm
from flask import render_template, request, flash, redirect, url_for
from app.models import User, Pokemon, PokemonTrainer
from flask_login import current_user, login_required
import requests


@bat.route('/pokesearch', methods=['GET', 'POST'])
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


@bat.route('/my_pokeballs')
@login_required
def my_pokeballs():
    # get all the pokemon caught for the person using my site
    poke = current_user.pokeballs
    return render_template('my_pokeballs.html.j2', poke = poke)

@bat.route('/training/<int:id>', methods = ['GET', 'POST'])
@login_required
def training(id):
    is_added = Pokemon.query.get(id)
    if len(current_user.pokeballs.all()) == 5:
        flash('Your pokeballs are full.', 'danger')
        return redirect(url_for('battle.my_pokeballs'))
    elif is_added:
        current_user.catch(is_added)
        flash("You have caught the Pokemon!", "success")
        return redirect(url_for('battle.my_pokeballs'))
    else:
        flash("Oh no! It escaped!", "warning")
        return redirect(url_for('battle.pokesearch'))

    
@bat.route('/release/<int:id>')
@login_required
def release(id):
    is_freed = Pokemon.query.get(id)
    current_user.free(is_freed)
    flash(f"You have freed the Pokemon.", "success")
    return redirect(url_for('battle.my_pokeballs'))

@bat.route('/battle/<int:id>')
@login_required
def battle(id):
    user_to_battle = User.query.get(id)
    current_user.battle(user_to_battle)
    poke = Pokemon.query.filter_by(id=id).first()
    flash(f"You have challanged {user_to_battle.first_name} {user_to_battle.last_name} to a battle!", "success")
    return render_template('battle_pokemon.html.j2', poke = poke, user_to_battle = user_to_battle)

@bat.route('/battle_results/<int:id>')
@login_required
def battle_results(id):
    user = User.query.get(id)
    if int(current_user.attack_power()) > int(user.attack_power()):
        current_user.wins += 1
        user.losses += 1
        user.save()
        current_user.save()
        flash(f"Player {current_user.first_name} has won! Congradulations!", "success")
        return redirect(url_for('main.show_players'))
    elif int(current_user.attack_power()) < int(user.attack_power()):
        current_user.losses += 1
        user.wins += 1
        user.save()
        current_user.save()
        flash(f"Player {user.first_name} has won! Better luck next time!", "danger")
        return redirect(url_for('main.show_players'))
    else:
        flash(f"Player {current_user.first_name} and Player {user.first_name} have tied!", "warning")
        return redirect(url_for('main.show_players'))
