from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from website.models import User, Expense
from website import db


class Registration(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])    
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    income = FloatField('Monthly Income', validators=[DataRequired()])    
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken')


class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AddExpense(FlaskForm):
    name = StringField('Name of Expense', validators=[DataRequired()])    
    price = FloatField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])    
    submit = SubmitField('Submit')

class AddGoal(FlaskForm):
    description = TextAreaField('Describe Your Goal', validators=[DataRequired()])    
    completed = BooleanField('Completed?')
    submit = SubmitField('Submit')
