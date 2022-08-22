import datetime
import random

from flask_login import current_user
from main.Core.Db_Core import Public_Service
from main.DataLayer.Core.User_Services import User_Service
from main.DataLayer.Database.models import Bank, Card
from main.Route.BankTransaction.tools import Transaction_Tools


class Balance_Calculate:
    def Plus(num1=float, num2=float):
        return num1 + num2

    def Minuse(num1=float, num2=float):
        return num1 - num2


class Card_Tools:

    global P_Service

    def Build_New_Card(bank_account):
        P_Service = Public_Service(Card)
        card_numbers = []
        for num in range(4):
            number = random.randint(1000, 9999)
            if number not in card_numbers:
                card_numbers.append(number)

        card = Card(fullname=bank_account.fullname,
                    card_number='{} {} {} {}'.
                    format(card_numbers[0], card_numbers[1],
                           card_numbers[2], card_numbers[3]),
                    card_cvv2=random.randint(1, 999),
                    card_expire_time=datetime.date(2420, 1, 24),
                    card_password=bank_account.password,
                    bank_accounts=bank_account,
                    user=current_user
                    )
        P_Service.Add_To(card)
        return True

    @staticmethod
    def Is_Ok_Balance_To_Purchased(bank_account, price=int):
        Transaction_T = Transaction_Tools()
        bank_card = User_Service.Get_BankCard_By_BankAccount(bank_account)
        P_Service = Public_Service(Bank)
        if bank_account.balance == 0 or bank_account.balance < price:
            return False
        bank_account.balance = bank_account.balance - price
        Transaction_T.Do_Transaction(current_bank_account=bank_account,
                                     bank_card=bank_card,purchase=price)
        P_Service.Save_Changes()
        return True
