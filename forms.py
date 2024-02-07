from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, validators

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    password = PasswordField("Password", [validators.DataRequired(), validators.Length(min=8, max=15)])

class RegisterForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    password = PasswordField("Password", [validators.DataRequired(), validators.Length(min=8, max=15)])
    confirm = PasswordField("Repeat password", [validators.EqualTo('password', message="Las contraseñas deben ser iguales")])

class CreateBlog(FlaskForm):
    title = StringField("Title", [validators.Length(min=4, max=25)])
    content = TextAreaField("Content", [validators.length(min=2)])