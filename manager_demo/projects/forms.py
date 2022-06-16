from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired

from manager_demo.models import Project


class NewProjectForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(max=512)])
    title = StringField('Title',
                           validators=[DataRequired(), Length(max=512)])
    short_name = StringField('Short name',
                           validators=[DataRequired(), Length(max=3,min=3)])
    description = TextAreaField('Description',validators=[Length(max=2048)])
    fps = SelectField('Frame rate', coerce=float, validators=[InputRequired()])
    production_type = SelectField('Production type', coerce=str, validators=[InputRequired()])
    submit = SubmitField('Create project')

    def validate_name(self, name):
        project = Project.query.filter_by(name=name.data).first()
        if project:
            raise ValidationError('Name already taken. Please choose another one.') 
    
    def validate_title(self, title):
        project = Project.query.filter_by(title=title.data).first()
        if project:
            raise ValidationError('Title already taken. Please choose another one.')

    def validate_short_name(self, short_name):
        project = Project.query.filter_by(short_name=short_name.data).first()
        if project:
            raise ValidationError('Short_name already taken. Please choose another one.')


class EditProjectForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(max=512)])
    title = StringField('Title',
                           validators=[DataRequired(), Length(max=512)])
    short_name = StringField('Short name',
                           validators=[DataRequired(), Length(max=3,min=3)])
    description = TextAreaField('Description',validators=[Length(max=2048)])
    fps = SelectField('Frame rate', coerce=float, validators=[InputRequired()])
    production_type = SelectField('Production type', coerce=str, validators=[InputRequired()])
    submit = SubmitField('Update')

    def __init__(self, project : Project, *args, **kwargs, ):
        FlaskForm.__init__(self, *args, **kwargs)
        self.project = project

    def validate_name(self, name):
        if name.data != self.project.name:
            project = Project.query.filter_by(name=name.data).first()
            if project:
                raise ValidationError('Name already taken. Please choose another one.') 
    
    def validate_title(self, title):
        if title.data != self.project.title:
            project = Project.query.filter_by(name=title.data).first()
            if project:
                raise ValidationError('Title already taken. Please choose another one.')

    def validate_short_name(self, short_name):
        if short_name.data != self.project.short_name:
            project = Project.query.filter_by(name=short_name.data).first()
            if project:
                raise ValidationError('Short_name already taken. Please choose another one.')

class ProjectUserForm(FlaskForm):
    user = SelectField('User', coerce=str, validators=[InputRequired()])
    submit_user = SubmitField('Assign to project')