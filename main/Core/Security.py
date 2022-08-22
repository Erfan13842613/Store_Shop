import re
from itsdangerous import URLSafeTimedSerializer
from main import app
from random import randint


class Security_Validator:

    @staticmethod
    def Validate_Email(email):
        # ([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+
        pattern = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+$')
        if re.fullmatch(pattern, email):
            return True
        return False


class Email_Token_Security:

    @staticmethod
    def Generate_Token(email):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return serializer.dumps(email, salt=bytes(app.config['SECURITY_PASSWORD_SALT']))

    @staticmethod
    def Confrim_Token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except Exception as e:
            return False
        return email

    @staticmethod
    def Generate_Random_Secret_Key(min, max):
        return randint(min, max)
