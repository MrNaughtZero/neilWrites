from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SelectField, TextAreaField
from wtforms.validators import InputRequired, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask import request
from app.models import Category

## Validators

def validate_length(name, value):
    def _length(FlaskForm, field):
        if len(field.data) < value:
            raise ValidationError(f'{name} must be a minimum {value} characters')
    return _length

def validate_passwords(FlaskForm, field):
    if field.data != request.form.get('password'):
        raise ValidationError('Passwords do not match')

## End of validators

## Custom DB query 

def category_choices():  
    return Category.query.all()

## end of DB query

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), validate_length('Username', 3)])
    password = PasswordField(validators=[InputRequired(), validate_length('Password', 8)])
    confirm_password = PasswordField(validators=[InputRequired(), validate_passwords])

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])

class CategoryForm(FlaskForm):
    category = StringField('Category Name', validators=[InputRequired(), validate_length('Category', 3)])

class PostForm(FlaskForm):
    title = StringField('Post Name', validators=[InputRequired(), validate_length('Post Title', 3)])
    category = QuerySelectField('Post Category', validators=[InputRequired()], query_factory=category_choices, get_label='cat')
    status = SelectField('Post Status', validators=[InputRequired()], choices=[('Published', 'Published'), ('Draft', 'Draft')])
    content = TextAreaField('Post Content')