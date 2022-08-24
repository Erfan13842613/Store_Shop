from main.Core.Db_Core import Public_Service, Security
from main.Core.Security import Email_Token_Security
from main.DataLayer.Database.models import User


class Admin:

    global Securities, Pu_Service

    def __init__(self, username, password) -> None:
        Securities = Email_Token_Security()
        self.username = username+'Admin'
        self.password = password
        self.email = username+"_Admin@gmail.com"
        self.secret_code = Securities.Generate_Random_Secret_Key(1, 10000)
        self.user_is_active = 1
        self.role = 'ADMIN'

    def Create_Admin(self):
        Securities = Security(User)
        Pu_Service = Public_Service(User)
        user = User(username=self.username,
                    email=self.email,
                    password=Securities.Hash_Password(self.password),
                    role=self.role,
                    user_is_active=self.user_is_active,
                    secret_code=self.secret_code)
        Pu_Service.Add_To(user)
        return True


obj_instance = Admin('Erfan', 261384)
obj_instance.Create_Admin()
print('Username : '+obj_instance.username +
      ' Password : ' + obj_instance.password)
