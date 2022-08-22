from main import db
class db_Tools:
    def Create_All_Tables():
        db.create_all()
        return True