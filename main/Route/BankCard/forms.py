from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.DataLayer.Core.User_Services import User_Service
from main.DataLayer.Database.models import Card, User


class Card_Purchase(FlaskForm):
    card_number = StringField('Card Number', validators=[DataRequired(
        'This Field Is Required')])
    card_cvv2 = StringField('Card Number', validators=[DataRequired(
        'This Field Is Required')])
    card_password = StringField('Card Number', validators=[DataRequired(
        'This Field Is Required')])
    submit = SubmitField('Purchase')

    def validate_card_number(self, card_number):
        user_card = Card.query.filter_by(user=current_user).first()
        
        if user_card is None:
            raise ValidationError('You Have No Card Account')
        elif user_card.card_number != card_number.data:
           raise ValidationError('This Card Number Is Invalid , Please Check Them')
       

    def validate_card_cvv2(self, card_cvv2):
        user_card = Card.query.filter_by(user=current_user).first()
 
        if user_card is None:
            raise ValidationError('You Have No Card Account')       
        elif user_card.card_cvv2 != card_cvv2.data:
           raise ValidationError('This Card Cvv2 Is Invalid , Please Check Them')
    
    def validate_card_password(self, password):
        user_card = Card.query.filter_by(user=current_user).first()
        
        if user_card is None:
            raise ValidationError('You Have No Card Account')
        elif user_card.card_password != password.data:
           raise ValidationError('This Card Password Is Invalid , Please Check Them')
    