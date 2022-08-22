from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,IntegerField,TextAreaField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.DataLayer.Core.User_Services import User_Service
from main.DataLayer.Database.models import User

class Build_New_Product_Form(FlaskForm):
    product_name=StringField('Product Name', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght')])
    product_gender=StringField('Product Gender', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght')])
    product_price=IntegerField('Product Price', validators=[DataRequired(
        'This Field Is Required')])
    product_summary=TextAreaField('Product Summary', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght')])
    submit=SubmitField('Create')