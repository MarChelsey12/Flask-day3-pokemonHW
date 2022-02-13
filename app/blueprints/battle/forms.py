from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import  InputRequired

class PokeForm(FlaskForm):
    #field name = datatypeField('LABEL', validators=[LIST OF validators])
    pokemon = StringField('Pokemon', validators=[InputRequired()])
    submit = SubmitField('Search')
