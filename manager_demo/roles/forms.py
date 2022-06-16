from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from manager_demo.models import Role


class NewRoleForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(max=64)])
    level = IntegerField('Level', [NumberRange(min=0, max=100)])
    description = TextAreaField('Description',validators=[Length(max=2048)])
    submit = SubmitField('Create role')

    def validate_name(self, name):
        role = Role.query.filter_by(name=name.data.lower()).first()
        if role:
            raise ValidationError('Name already taken. Please choose another one.') 

class EditRoleForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(max=64)])
    level = IntegerField('Level', [NumberRange(min=0, max=100)])
    description = TextAreaField('Description',validators=[Length(max=2048)])
    submit = SubmitField('Update role')