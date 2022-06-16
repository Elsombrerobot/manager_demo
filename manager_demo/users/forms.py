from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired

from manager_demo.models import Role


class NewUserForm(FlaskForm):
    first_name = StringField('First name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Create user')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EditUserForm(FlaskForm):
    first_name = StringField('First name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password',
                                     validators=[EqualTo('password')])
    picture = FileField('Update profile picture',
                        validators=[FileAllowed(["jpeg", "jpg", "png", "JPEG", "PNG", "JPG"])])
    submit_update = SubmitField('Update user')

class UserRoleForm(FlaskForm):
    role = SelectField('Role', coerce=str, validators=[InputRequired()])
    submit_role = SubmitField('Assign role')

class UserProjectForm(FlaskForm):
    project = SelectField('Project', coerce=str, validators=[InputRequired()])
    submit_project = SubmitField('Assign to project')


