from app import db, login
from flask_login import UserMixin # This is just for the User model!
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class Pokemon(db.Model):
    __tablename__ = 'pokemon'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True) 
    base_xp = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    p_type = db.Column(db.String)
    ability = db.Column(db.String)
    move = db.Column(db.String)
    sprite = db.Column(db.String)

    def from_dict(self, data):
        self.name = data['name']
        self.base_xp = data['base_xp']
        self.weight = data['weight']
        self.p_type = data['p_type']
        self.ability = data['ability']
        self.move = data['move']
        self.sprite = data['sprite']

    # saves the pokemon to the database
    def save(self):
        db.session.add(self) # add the pokemon to the db session
        db.session.commit() #save everything in the session to the database

    def remove(self):
        db.session.delete(self)
        db.session.commit()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    bio = db.Column(db.String(300))
    icon = db.Column(db.Integer)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    pokeballs = db.relationship('Pokemon',
                    secondary = 'pokemon_trainer',
                    backref='trainer',
                    lazy='dynamic',
                    )

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'
        
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
        self.bio = data['bio']
        self.icon = data['icon']
        self.wins = data['wins']
        self.losses = data['losses']

    # saves user to database
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def get_icon_url(self):
        return f'https://avatars.dicebear.com/api/adventurer/{self.icon}.svg'
        
    def catch(self, pokemon):
        self.pokeballs.append(pokemon)
        db.session.commit()

    def free(self, pokemon):
        self.pokeballs.remove(pokemon)
        db.s
        
    def battle(self, trainer):
        return self.pokeballs.filter(self.id == trainer.id)

    def attack_power(self):
        attack = []
        for poke in self.pokeballs:
            attack.append(int(poke.base_xp))
        attack_total = sum(attack)
        return str(attack_total)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class PokemonTrainer(db.Model):
    __tablename__ = 'pokemon_trainer'
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def __repr__(self):
        return f'<PokemonTrainer: {self.pokemon_id} | {self.trainer_id}>'
