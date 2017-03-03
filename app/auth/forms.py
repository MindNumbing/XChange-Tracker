from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from wtforms.validators import DataRequired


class SignupForm(Form):

    username = StringField('Username',
                           [validators.required(),
                            validators.Length(min=6, max=64)])

    email = StringField('Email Address',
                        [validators.required(),
                         validators.Length(min=6, max=64)])

    password = PasswordField('Password',
                             [validators.required(),
                              validators.length(min=10, max=64),
                              PasswordField()])

    confirm_password = PasswordField('Confirm Password',
                                     [validators.required(),
                                      validators.length(min=10, max=64),
                                      PasswordField(),
                                      validators.equal_to('Password',
                                      message='Password and Confirm Password must be the same')])


class LoginForm(Form):
    username = StringField('Username',
                           [DataRequired(message='Username required'),
                            validators.Length(min=4, max=60)])

    password = PasswordField('Password',
                             [DataRequired(message='Password required'),
                              validators.Length(min=6, max=200)])
