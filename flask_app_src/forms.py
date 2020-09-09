from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired


class MakeOrderForm(FlaskForm):
    text = TextAreaField('Input your text', validators=[DataRequired()])
    lang = RadioField('Choose language',
                      choices=[
                          (1, 'Русский'),
                          (2, 'Українська'),
                          (3, 'English'),
                      ],
                      default=1,
                      validators=[DataRequired()])
    send = SubmitField('Send')
