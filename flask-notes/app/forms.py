from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=3, max=64)
    ])
    email    = StringField('Email', validators=[
        DataRequired(), Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6)
    ])
    confirm  = PasswordField('Confirm password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    submit   = SubmitField('Register')

    # custom validator — Flask-WTF auto-calls any method named validate_<fieldname>
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken.')


class LoginForm(FlaskForm):
    email    = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit   = SubmitField('Login')


class NoteForm(FlaskForm):
    title   = StringField('Title', validators=[DataRequired(), Length(max=140)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit  = SubmitField('Save note')