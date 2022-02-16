from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email, InputRequired
from app.models import User
import random
from jinja2 import Markup



class LoginForm(FlaskForm):
    #field name = DatatypeField('LABEL', validators=[LIST OF validators])
    email = StringField('Email Address',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[Email(),DataRequired()])
    bio = StringField('Bio')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    # https://avatars.dicebear.com/api/adventurer/123.svg
    m1= random.randint(1,1000)
    m2= random.randint(1001,2000)
    m3= random.randint(2001,3000)
    m4= random.randint(3001,4000)
    m5= random.randint(4001,5000)

    m1_img= Markup(f'<img src="https://avatars.dicebear.com/api/adventurer/{m1}.svg" style="height:75px">')
    m2_img= Markup(f'<img src="https://avatars.dicebear.com/api/adventurer/{m2}.svg" style="height:75px">')
    m3_img= Markup(f'<img src="https://avatars.dicebear.com/api/adventurer/{m3}.svg" style="height:75px">')
    m4_img= Markup(f'<img src="https://avatars.dicebear.com/api/adventurer/{m4}.svg" style="height:75px">')
    m5_img= Markup(f'<img src="https://avatars.dicebear.com/api/adventurer/{m5}.svg" style="height:75px">')

    icon = RadioField('Avatar', validators=[DataRequired()], choices=[(m1, m1_img),(m2, m2_img),(m3, m3_img),(m4, m4_img),(m5, m5_img)])

    def validate_email(form, field):
        same_email_user = User.query.filter_by(email = field.data).first()
        if same_email_user:
            raise ValidationError('Email is already in use.')

class EditProfileForm(FlaskForm):
    first_name= StringField('First Name',validators=[DataRequired()])
    last_name= StringField('Last Name',validators=[DataRequired()])
    email = StringField('Email Address',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    bio = StringField('Bio')
    submit = SubmitField('Update')

    m1= random.randint(1,1000)
    m2= random.randint(1001,2000)
    m3= random.randint(2001,3000)
    m4= random.randint(3001,4000)
    m5= random.randint(4001,5000)

    m1_img= Markup(f'<img src="https://avatars.dicebear.com/api/adventurer/{m1}.svg" style="height:75px">')
    m2_img= Markup(f'<img src="https://avatars.dicebear.com/api/adventurer/{m2}.svg" style="height:75px">')
    m3_img= Markup(f'<img src="https://avatars.dicebear.com/api/adventurer/{m3}.svg" style="height:75px">')
    m4_img= Markup(f'<img src="https://avatars.dicebear.com/api/adventurer/{m4}.svg" style="height:75px">')
    m5_img= Markup(f'<img src="https://avatars.dicebear.com/api/adventurer/{m5}.svg" style="height:75px">')

    icon = RadioField('Choose an Avatar', validators=[DataRequired()], choices=[(9000, "Keep the same"),(m1, m1_img),(m2, m2_img),(m3, m3_img),(m4, m4_img),(m5, m5_img)])
