from main import db, bcrypt


class Data_Service:
    def __init__(self, Table) -> None:
        self.table = Table
        return self


class Public_Service(Data_Service):
    def __init__(self, Table) -> None:
        super().__init__(Table)

    def Get_By_Id(self, id):
        return self.table.query.get(id)

    def Get_By_Id_Or_404(self, id):
        return self.table.query.get_or_404(id)

    @staticmethod
    def Add_To(value):
        db.session.add(value)
        Public_Service.Save_Changes()
        return True

    @staticmethod
    def Del_To(value):
        db.session.delete(value)
        Public_Service.Save_Changes()
        return True

    @staticmethod
    def Save_Changes():
        db.session.commit()
    
    @staticmethod
    def Delete_All(value):
        for item in value:
            Public_Service.Del_To(item)

    def Get_All(self):
        return self.table.query.all()


class Security(Data_Service):
    def __init__(self, Table) -> None:
        super().__init__(Table)

    @staticmethod
    def Hash_Password(password):
        return bcrypt.generate_password_hash(password)

    @staticmethod
    def Check_Password_Matching(obj_mod, password):
        return obj_mod and bcrypt.check_password_hash(obj_mod.password, password)

    