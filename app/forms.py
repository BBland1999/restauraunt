from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, HiddenField
from wtforms.validators import DataRequired, EqualTo
from app.models import My_User

class Username_Password():
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class LoginForm(FlaskForm, Username_Password):
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm, Username_Password):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = My_User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_phone(self, phone):
        p = phone.data
        if not p.isdigit():
            raise ValidationError('Phone number must be a number.')

        user = My_User.query.filter_by(phone=p).first()
        if user is not None:
            raise ValidationError('Please use a different phone number.')

class SubmitOrder(FlaskForm):
    submit = SubmitField('Submit Order')

