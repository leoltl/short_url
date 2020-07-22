from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class MainURLForm(FlaskForm):
  fullUrl = StringField(
    "Full Url", 
    validators=[DataRequired()], 
    render_kw={"placeholder": 'Shorten your link'})
  submit = SubmitField("Shorten URL")