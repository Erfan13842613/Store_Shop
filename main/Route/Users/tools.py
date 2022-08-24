from flask_login import current_user, login_user
from main.Core.Db_Core import Public_Service, Security
from main.Core.Security import Email_Token_Security
from main.DataLayer.Core.User_Services import User_Service
from main.DataLayer.Database.models import User
import requests
import time
import json


class User_Tools:
    global Db_Sec, D_Service, P_Service, Sec_Service

    @staticmethod
    def Login_User(form):
        Db_Sec = Security(User)
        D_Service = User_Service()
        user = D_Service.Get_User_By_Email(form.email.data)
        if user and Db_Sec.Check_Password_Matching(user, form.password.data):
            login_user(user)
            return user
        else:
            return False

    @staticmethod
    def SignUp_User(form):
        Db_Sec = Security(User)
        P_Service = Public_Service(User)
        Sec_Service = Email_Token_Security()
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=Db_Sec.Hash_Password(form.password.data),
                    role="SELLER" if form.role.data else "USER",
                    secret_code=Sec_Service.Generate_Random_Secret_Key(40000, 60000))
        P_Service.Add_To(user)
        return user

    @staticmethod
    def Change_UserPassword(form):
        Db_Sec = Security(User)
        D_Service = User_Service()
        P_Service = Public_Service(User)
        user = D_Service.Get_User_By_Email(current_user.email)
        if Db_Sec.Check_Password_Matching(user, form.old_password.data):
            user.password = Db_Sec.Hash_Password(form.new_password.data)
            P_Service.Save_Changes()
            return True
        return False

    @staticmethod
    def Send_Sms(user):
        P_Service = Public_Service(User)
        Sec_Service = Email_Token_Security()
        user.secret_code = Sec_Service.Generate_Random_Secret_Key(40000, 60000)
        P_Service.Save_Changes()

        url = "https://sms-wrapper-uat.k8s.daan.ir/api/v1/sms/send?sms_service_id=0"
        phone_number = f"{user.phone}".replace('0', '98', 1)
        payload = json.dumps({
            "msisdn": "{}".format(phone_number),
            "message": f"Thanks For Registering In This Site .Your Active Code Is : {user.secret_code}"
        })
        headers = {
            'X-API-KEY': '11111',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        user.secret_code = Sec_Service.Generate_Random_Secret_Key(40000, 60000)
        P_Service.Save_Changes()

    @staticmethod
    def Is_Account_Active(user):
        if user.user_is_active == 0:
            return True
        return False

