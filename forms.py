from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, IntegerField, validators, SelectField, SubmitField

class RegistrationForm(FlaskForm):
    #car     = StringField('Make & Model', [validators.Length(min=4, max=25)])
    car = SelectField('Make & Model', default="Toyota Corolla", validators=[validators.DataRequired()])
    #year = SelectField('Year')
    #accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])
    submit = SubmitField('Submit')


class OtherForm(FlaskForm):
    #car     = StringField('Make & Model', [validators.Length(min=4, max=25)])
    car = SelectField('Make & Model', validators=[validators.DataRequired()])
    year = SelectField('Year', default=2015, validators=[validators.DataRequired()])
    #accept_rules = BooleanField('I accept the site rules', [validators.DataRequired()])
    submit = SubmitField('Submit')