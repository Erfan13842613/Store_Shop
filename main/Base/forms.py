from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.DataLayer.Core.Bank_Services import Bank_Service
from main.DataLayer.Core.User_Services import User_Service
from main.DataLayer.Database.models import Bank

class Search_For_User_Form(FlaskForm):
    fullname=StringField('Card Number', validators=[DataRequired(
        'This Field Is Required')])
    submit=SubmitField('Search')