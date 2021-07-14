# -*- coding: utf-8 -*-

import sqlite3
import abc

class ATM:
    def __init__(self, Display, Validation, Feature):
        self.Display = Display
        self.Validation = Validation
        self.Feature = Feature

    def run(self):
        T = 1
        while T:
            cardno, Pass = self.Display.FirstScreen()
            check = self.Validation.check(cardno, Pass)
            if check:
                id, cardno, cardpin, balance, username, status, cardlimit, typeofaccount = self.Validation.getDetails(
                    cardno)
                userobj = Account(id, cardno, cardpin, balance, username, status, cardlimit, typeofaccount)
                self.Feature.SecondScreen(userobj)
            else:
                continue


class Account:
    def __init__(self, id, cardno, cardpin, balance, username, status, cardlimit, typeofaccount):
        self.__id = id
        self.__cardno = cardno
        self.__cardpin = cardpin
        self.__balance = balance
        self.__username = username
        self.__status = status
        self.__cardlimit = cardlimit
        self.__typeofaccount = typeofaccount

    def getUserId(self):
        return self.__id

    def getStatus(self):
        return self.__status

    def updateBalance(self, amount):
        self.__balance = amount

    def updateStatus(self, status):
        self.__status = status


class Display:
    def FirstScreen(self):
        print("WELCOME TO APNA BANK")
        print("LOGIN VERIFICATION")
        card_no = input("Enter Card No")
        pin = input("Enter Pin")
        return card_no, pin


class Validation:
    def check(self, cardno, Pass):
        card_num = cardno
        pin_num = Pass
        if card_num.isnumeric() and pin_num.isnumeric():
            conn = sqlite3.connect("ATMSYS.s3db")
            cur = conn.cursor()
            query = f'''select count(*) from users where cardno = {card_num} and cardpin = {pin_num} and status = 'ACTIVE' '''
            cur.execute(query)
            count = cur.fetchall()
            if count[0][0] == 1:
                query = f'''select id,username from users where cardno = {card_num} and cardpin = {pin_num}'''
                cur.execute(query)
                id = cur.fetchall()
                ret = True
                user_id = id[0][0]
                print("\nWelcome to the ATM services", id[0][1], "!!\n")
            else:
                print("Either your card is blocked or you entered wrong credentials")
                user_id = 0
                ret = False
            # closing the connection
            conn.commit()
            conn.close()
        else:
            print("Entered value is not numeric")
            ret = False
        return ret

    def getDetails(self, cardno):
        conn = sqlite3.connect("ATMSYS.s3db")
        cur = conn.cursor()
        card_num = cardno
        query = f'''select * from users where cardno = {card_num} '''
        cur.execute(query)
        detail = cur.fetchall()
        id = detail[0][0]
        cardno = detail[0][1]
        cardpin = detail[0][2]
        balance = detail[0][3]
        username = detail[0][4]
        status = detail[0][6]
        cardlimit = detail[0][7]
        typeofaccount = detail[0][8]
        conn.close
        return id, cardno, cardpin, balance, username, status, cardlimit, typeofaccount

class ATMdisplay(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def SecondScreen(self,userobj):
        pass

    @abc.abstractmethod
    def TransThirdScreen(self,userobj):
        pass

    @abc.abstractmethod
    def AccThirdScreen(self,userobj):
        pass

    @abc.abstractmethod
    def SetThirdScreen(self,userobj):
        pass

class Feature(ATMdisplay):
    def __init__(self, Withdraw, Deposit, Transfer, Card_limit, Blockedcards, CardPin, Transaction_details):
        self.Withdraw = Withdraw
        self.Deposit = Deposit
        self.Transfer = Transfer
        self.Card_limit = Card_limit
        self.Blockedcards = Blockedcards
        self.CardPin = CardPin
        self.Transaction_details = Transaction_details

    def SecondScreen(self, userobj):
        T = 1
        while T == 1:
            print(" Press 1. for Transactions")
            print(" Press 2. for Account Details")
            print(" Press 3. for Settings")
            print(" Press 4. to Exit")
            choice = input()
            if choice.isnumeric():
                choice = int(choice)
                if choice == 1:
                    self.TransThirdScreen(userobj)
                if choice == 2:
                    self.AccThirdScreen(userobj)
                if choice == 3:
                    self.SetThirdScreen(userobj)
                if choice == 4:
                    print("Exiting..")
                    T = 0
                else:
                    T = 0
                    print("Not a correct choice.")
            else:
                print("Entered value is not numeric")

    def TransThirdScreen(self, userobj):
        T = 1
        while T == 1:
            print(" Press 1. for Withdrawl")
            print(" Press 2. for Transfer")
            print(" Press 3. for Deposit")
            print(" Press 4. to Exit")
            choice = input()
            if choice.isnumeric():
                choice = int(choice)
                if choice == 1:
                    self.Withdraw.withdrawl(userobj)
                if choice == 2:
                    self.Transfer.transact(userobj)
                if choice == 3:
                    self.Deposit.deposit_money(userobj)
                if choice == 4:
                    print("Exiting..")
                    T = 0
                else:
                    T = 0
                    print("Enter a valid choice")
            else:
                print("Entered choice not numeric")
    def AccThirdScreen(self, userobj):
        T = 1
        while T == 1:
            print(''' 
      1. Mini Statement
      2. Linked Cards 
      3. Last Transaction 
      4. Balance Enquiry 
      5. Go Back to the previous menu''')
            choice = input()
            if choice.isnumeric():
                choice = int(choice)
                if choice == 1:
                    self.Transaction_details.Mini_Statement(userobj)
                if choice == 2:
                    self.Transaction_details.Linked_Cards(userobj)
                if choice == 3:
                    self.Transaction_details.Last_Transaction_detail(userobj)
                if choice == 4:
                    self.Transaction_details.Balance_Enquiry(userobj)
                if choice == 5:
                    print("Exiting..")
                    T = 0
                else:
                    T = 0
                    print("Not a valid choice")
            else:
                print("entered choice not numeric")
    def SetThirdScreen(self, userobj):
        T = 1
        while T == 1:
            print('''
          1. Set Limit 
          2. Block Card 
          3. Change Pin 
          4. Go Back to the previous menu''')
            choice = input()
            if choice.isnumeric():
                choice = int(choice)
                if choice == 1:
                    self.Card_limit.set_card_limit(userobj)
                if choice == 2:
                    self.Blockedcards.blockCards(userobj)
                if choice == 3:
                    self.CardPin.change_pin(userobj)
                if choice == 4:
                    print("Exiting..")
                    T = 0
                else:
                    T = 0
                    print("Not a valid choice")
            else:
                print("Not a valid choice")

class Transactions:
    def Check_Balance_Amount(self, userobj, Account_type):
        user_id = userobj.getUserId()
        conn = sqlite3.connect("ATMSYS.s3db")
        cur = conn.cursor()
        query = f'''select balance from users where id={user_id} and typeofaccount="{Account_type}"'''
        cur.execute(query)
        balance_amount = cur.fetchall()
        return balance_amount[0][0]

    def print_updated_balance(self, userobj, Account_type):
        user_id = userobj.getUserId()
        conn = sqlite3.connect("ATMSYS.s3db")
        cur = conn.cursor()
        query = f'''select balance from users where id={user_id} and typeofaccount="{Account_type}"'''
        cur.execute(query)
        balance1 = cur.fetchall()
        print("your current account balance is", balance1[0][0])
        conn.commit()
        conn.close()

    def View_Limit(self, userobj, Account_type):
        user_id = userobj.getUserId()
        conn = sqlite3.connect("ATMSYS.s3db")
        cur = conn.cursor()
        query = f'''select cardlimit from users where id={user_id} and typeofaccount="{Account_type}"'''
        cur.execute(query)
        limit = cur.fetchall()
        return limit[0][0]

    def Select_Account_Type(self):
        type1 = int(input("Select Account Type.\n Press 1 for Savings account and 2 for Current Account"))
        return type1

    def Status(self, userobj):
        user_id = userobj.getUserId()
        conn = sqlite3.connect("ATMSYS.s3db")
        cur = conn.cursor()
        query1 = f'''select * from users where id = {user_id} and status = "ACTIVE"'''
        cur.execute(query1)
        row = cur.fetchall()
        return row


class withdraw(Transactions):
    def withdrawl(self, userobj):
        user_id = userobj.getUserId()
        row = self.Status(userobj)
        if row != []:
            Amount = input("\nEnter cash amount to withdraw in 10 denomination:\n")
            if not Amount.isnumeric():
                print("Amount not a number, Enter Amount in 10 denomination")
                return
            Amount = float(Amount)
            # To check if the amount is in 10 denomination
            if Amount % 10 != 0 or Amount < 0:
                print()
                print('AMOUNT  MUST BE IN 10 DENOMINATION')
                print()
            else:
                conn = sqlite3.connect("ATMSYS.s3db")
                cur = conn.cursor()
                # Select_Account_Type() is called to get input from user where the withdrawl is to be performed
                type = self.Select_Account_Type()
                if type == 1:
                    typeofaccount1 = "SAVINGS"
                if type == 2:
                    typeofaccount1 = "CURRENT"
                limit1 = int(self.View_Limit(userobj, typeofaccount1))
                balance1 = self.Check_Balance_Amount(userobj, typeofaccount1)

                # The withdrawl occurs only if the balance after subtracting the withdrawl amount does not go beyond the limit that is set
                if balance1 - Amount > limit1:
                    query1 = f'''update users set balance = balance -  {Amount} where id = {user_id} and typeofaccount="{typeofaccount1}"'''
                    cur.execute(query1)
                    query2 = f'''select cardno ,balance from users where id="{user_id}" and typeofaccount="{typeofaccount1}" '''
                    cur.execute(query2)
                    cardno = cur.fetchall()
                    query3 = f'''insert into transactions (cardno ,transtype , amount, date, currenttime,current_balance ) values({cardno[0][0]} , 'DEBIT' , {Amount},CURRENT_DATE,CURRENT_TIME,{cardno[0][1]}) '''
                    cur.execute(query3)
                    userobj.updateBalance(balance1 - Amount)
                    print("Amount Debited Rs.", Amount, "from card no", cardno[0][0])
                    self.print_updated_balance(userobj, typeofaccount1)
                else:
                    print("The transaction was unsuccessful")
                conn.commit()
                conn.close()
        else:
            print("Card is Blocked. Visit Bank")


class Deposit(Transactions):
    def deposit_money(self, userobj):
        row = self.Status(userobj)
        if row != []:
            user_id = userobj.getUserId()
            Amount = input("\nEnter cash amount to deposit:\n")
            if not Amount.isnumeric():
                print("Entered amount is not numeric.")
                return
            if int(Amount) < 0 or int(Amount) % 10 != 0:
                print("Enter amount in 10 denomination ")
                return
            Amount = int(Amount)
            # account_type = int(input("\n Select account type \n Press 1 for SAVINGS and 2 for CURRENT account"))
            type1 = self.Select_Account_Type()
            if type1 == 1:
                typeofaccount2 = "SAVINGS"
            if type1 == 2:
                typeofaccount2 = "CURRENT"
            if Amount % 10 != 0:
                print()
                print('AMOUNT MUST BE IN 10 DENOMINATION')
                print()
            else:
                conn = sqlite3.connect("ATMSYS.s3db")
                cur = conn.cursor()
                # the balance is updated
                query = f'''update users set balance = balance +  {Amount} where id = {user_id} and  typeofaccount="{typeofaccount2}"'''
                cur.execute(query)
                query = f'''select cardno,balance from users where id="{user_id}" and  typeofaccount="{typeofaccount2}" '''
                cur.execute(query)
                cardno = cur.fetchall()
                if cardno == []:
                    # checks if the account entered is not there
                    print("Entered account type mismatch")
                    conn.commit()
                    conn.close()
                else:
                    # update the transaction table
                    query = f'''insert into transactions (cardno ,transtype , amount, date, currenttime,current_balance ) values({cardno[0][0]} , 'CREDIT' , {Amount},CURRENT_DATE,CURRENT_TIME,{cardno[0][1]}) '''
                    cur.execute(query)
                    conn.commit()
                    balance1 = self.Check_Balance_Amount(userobj, typeofaccount2)
                    userobj.updateBalance(balance1 - Amount)
                    print("Amount deposited Rs.", Amount, "to card no", cardno[0][0])
                    self.print_updated_balance(userobj, typeofaccount2)
                    conn.close()
        else:
            print("Card is Blocked. Visit Bank")


class Transfer_money(Transactions):
    def Beneficiary(self, userobj):
        user_id = userobj.getUserId()
        cardno = input("\nEnter Card Number:\n")
        Amount = input("\nEnter amount to transfer from your account:\n")
        if cardno.isnumeric() == False or Amount.isdecimal() == False:
            print(" Entered details not numeric")
            fine = False
            return fine, cardno, Amount
        cardno = int(cardno)
        Amount = float(Amount)
        if Amount < 0:
            fine = False
            return fine, cardno, Amount
        conn = sqlite3.connect("ATMSYS.s3db")
        cur = conn.cursor()
        query = f'''select balance , cardlimit from users where id="{user_id}" '''
        cur.execute(query)
        row = cur.fetchall()
        query = f'''select count(*) from users where cardno= "{cardno}" '''
        cur.execute(query)
        countno = cur.fetchall()
        # here also it is checked that the limit is not passed on the process of transfer
        if row[0][0] - Amount > row[0][1] and countno[0][0] == 1:
            fine = True
        else:
            fine = False
        conn.close()
        return fine, cardno, Amount

    def transact(self, userobj):
        user_id = userobj.getUserId()
        row = self.Status(userobj)
        if row != []:
            fine, cardno, Amount = self.Beneficiary(userobj)
            if fine:
                conn = sqlite3.connect("ATMSYS.s3db")
                cur = conn.cursor()
                query = f'''update users set balance = balance +  {Amount} where cardno = {cardno}'''
                cur.execute(query)
                query = f'''update users set balance = balance - {Amount} where id = {user_id}'''
                cur.execute(query)
                query1 = f'''select cardno,balance from users where id="{user_id}" '''
                cur.execute(query1)
                cardno_user = cur.fetchall()
                query2 = f'''select balance from users where cardno = "{cardno}"'''
                cur.execute(query2)
                benef = cur.fetchall()
                # updates the transaction table
                query = f'''insert into transactions (cardno ,transtype , amount, date, currenttime,current_balance ) values({cardno} , 'CREDIT' , {Amount},CURRENT_DATE,CURRENT_TIME,{benef[0][0]}) '''
                cur.execute(query)
                query = f'''insert into transactions (cardno ,transtype , amount, date, currenttime,current_balance )  values({cardno_user[0][0]} , 'DEBIT' , {Amount},CURRENT_DATE,CURRENT_TIME,{cardno_user[0][1]}) '''
                cur.execute(query)
                conn.commit()
                print("Amount transferred Rs.", Amount, "to card no", cardno, "from card no ", cardno_user[0][0])
                conn.close()
            else:
                print("Beneficiary details invalid")
        else:
            print("Card is Blocked. Visit Bank")


class Settings:
    def View_Limit1(self, userobj):
        user_id = userobj.getUserId()
        conn = sqlite3.connect("ATMSYS.s3db")
        cur = conn.cursor()
        query = f'''select cardlimit from users where id={user_id}'''
        cur.execute(query)
        limit = cur.fetchall()
        return limit[0][0]

    def Select_Account_Type(self):
        type1 = int(input("Select Account Type.\n Press 1 for Savings account and 2 for Current Account"))
        return type1

    def CardType(self):
        card = input("select the type of card you want to block.\n Press 1 for credit card and 2 for debit card")
        cardnumber = input("select the number of the card that you want to block")
        if card.isnumeric() and cardnumber.isnumeric():
            fine = True
            card = int(card)
            cardnumber = int(cardnumber)
        else:
            fine = False
        return fine, card, cardnumber

    def Check_status(self, userobj):
        user_id = userobj.getUserId()
        conn = sqlite3.connect("ATMSYS.s3db")
        cur = conn.cursor()
        query1 = f'''select status from users where id={user_id}'''
        cur.execute(query1)
        row = cur.fetchall()
        return row[0][0]

    def Status(self, userobj):
        user_id = userobj.getUserId()
        conn = sqlite3.connect("ATMSYS.s3db")
        cur = conn.cursor()
        query1 = f'''select * from users where id = {user_id} and status = "ACTIVE"'''
        cur.execute(query1)
        row = cur.fetchall()
        return row


class Card_Limit(Settings):
    def set_card_limit(self, userobj):
        user_id = userobj.getUserId()
        status = userobj.getStatus()
        if status == 'ACTIVE':
            ans = int(input("Do you want to see the limit that is initially set.Press 1 for yes and 2 for no"))
            if ans == 1:
                limit = self.View_Limit1(userobj)
                print("The limit set is", limit)
            else:
                print("\n Set Limit so that balance amount doesnt crosses the limit.\n")
                limit_set = input('\nEnter limit amount:\n')
                if limit_set.isnumeric():
                    limit_set = int(limit_set)
                    if limit_set > 0:
                        # For connecting to the database
                        conn = sqlite3.connect("ATMSYS.s3db")
                        cur = conn.cursor()
                        query = f'''update users set cardlimit = "{limit_set}" where id = "{user_id}" '''
                        # TO execute the sql query
                        cur.execute(query)
                        conn.commit()
                        conn.close()
                        print("\nlimit set successful!!\n")
                    else:
                        print("\nlimit can only be positive\n")
                    print("")
                else:
                    print("Entered limit is not numeric")
        else:
            print("Card Blocked. Visit Bank")

class BlockedCards(Settings):
    def blockCards(self, userobj):
        user_id = userobj.getUserId()
        row = self.Status(userobj)
        if row != []:
            conn = sqlite3.connect("ATMSYS.s3db")
            cur = conn.cursor()
            block = input("Press 1 for blocking current card and Press 2 for blocking any of the linked cards")
            # This part will block the current card
            if block.isnumeric():
                block = int(block)
                if block == 1:
                    status = self.Check_status(userobj)
                    if status == "ACTIVE":
                        query = f''' update users set status = 'BLOCK' where id = {user_id} '''
                        cur.execute(query)
                        print("The current card is blocked now")
                        userobj.updateStatus('BLOCK')
                # this part will block the any of the cards linked to this card
                if block == 2:
                    fine, card, cardnumber = self.CardType()
                    if fine:
                        query = f'''select cardno from users where id={user_id} '''
                        cur.execute(query)
                        row = cur.fetchall()
                        # This will block the credit card linked
                        if card == 1:
                            query = f''' update linkedcards set status = 'BLOCK' where cardno = "{row[0][0]}" and typeofcard="CREDIT CARD" and linkcardno="{cardnumber}"'''
                            cur.execute(query)
                            print("The linked card is blocked")
                        # This will block the debit card linked
                        if card == 2:
                            query = f''' update linkedcards set status = 'BLOCK' where cardno = "{row[0][0]}" and typeofcard="DEBIT CARD" and linkcardno="{cardnumber}"'''
                            cur.execute(query)
                            print("The linked card is blocked")
                        userobj.updateStatus('BLOCK')
                    else:
                        print("Entered value is not valid")
                else:
                    print("Sorry you could not proceed further")
                conn.commit()
                conn.close()
                print("")
            else:
                print("Not a valid choice")
        else:
            print("Card is Blocked. Visit Bank")


class CardPin(Settings):
    def change_pin(self, userobj):
        user_id = userobj.getUserId()
        row = self.Status(userobj)
        if row != []:
            old_pass = input("\nEnter old pin:\n")
            new_pass = input("\nEnter new pin:\n")
            conn = sqlite3.connect("ATMSYS.s3db")
            cur = conn.cursor()
            query = f'''select cardpin from users where id="{user_id}" '''
            cur.execute(query)
            row = cur.fetchall()
            # this checks if the old password entered is correct
            if row[0][0] == str(old_pass):
                # this checks if the new pin is all digits or not
                if not (new_pass.isdigit()):
                    print("ONLY DIGITS ARE ALLOWED IN PIN")
                    return
                # this ensures that the length of the pin should be 4
                if not (len(new_pass) == 4):
                    print("The length of pin must be 4 digits")
                else:
                    # the new pin is confirmed here before final updating
                    newppin = input("Please confirm the new pin")
                    if newppin != new_pass:
                        print("The confirmed pin does not match with the pin you entered before")
                    else:
                        query = f'''select cardpin from users where id="{user_id}" '''
                        cur.execute(query)
                        row = cur.fetchall()
                        query = f'''update users set cardpin = "{new_pass}" where id = "{user_id}" '''
                        cur.execute(query)
                        conn.commit()
                        conn.close()
                        print("Pin changed Successfully!!")
            else:
                print("old password entered is not correct ")
            print("")
        else:
            print("Card is Blocked. Visit Bank")


class AccountDetails:
    def period_of_statement(self):
        start_date = (input("Enter the start date.The date should be in YYYY-MM-DD format"))
        end_date = (input("Enter the end date.The date should be in YYYY-MM-DD format"))
        return start_date, end_date

    def Balance_Enquiry(self, userobj):
        user_id = userobj.getUserId()
        status = userobj.getStatus()
        if status == 'ACTIVE':
            decide = str(input("Do you want to proceed with it.Press Y fo yes and N For no"))
            if decide == 'Y' or decide == 'y':
                conn = sqlite3.connect("ATMSYS.s3db")
                cur = conn.cursor()
                query = f'''select balance from users where id = "{user_id}" '''
                cur.execute(query)
                row = cur.fetchall()
                print("your current account balance is", row[0][0])
                conn.commit()
                conn.close()
            else:
                print("Wrong Input")
        else:
            print("Card Blocked. Visit Bank.")

class Transaction_details(AccountDetails):
    def Mini_Statement(self, userobj):
        user_id = userobj.getUserId()
        status = userobj.getStatus()
        if status == 'ACTIVE':
            start, end = self.period_of_statement()
            conn = sqlite3.connect("ATMSYS.s3db")
            cur = conn.cursor()
            query = f'''select cardno from users where id="{user_id}" '''
            cur.execute(query)
            row = cur.fetchall()
            # this query ensures that the transactions are from start date to ernd date only
            query2 = f'''select * from transactions  where cardno="{row[0][0]}" and date>="{start}" and date<="{end}"'''
            cur.execute(query2)
            row2 = cur.fetchall()
            print("These are the transactions from start date to end date:")
            for i in range(0, len(row2)):
                print(i + 1, "CARD NO:", row2[i][0], " TYPE OF TRANSACTION:", row2[i][1], " TRANSACTION AMOUNT:",
                      row2[i][2], " DATE OF TRANSACTION:", row2[i][3], " TIME OF TRANSACTION:", row2[i][4],
                      "UPDATED BALANCE:", row2[i][5])

            conn.commit()
            conn.close()
        else:
            print("Card blocked. Please Visit Bank")
    def Last_Transaction_detail(self, userobj):
        user_id = userobj.getUserId()
        status = userobj.getStatus()
        if status == 'ACTIVE':
            conn = sqlite3.connect("ATMSYS.s3db")
            cur = conn.cursor()
            query = f'''select cardno from users where id="{user_id}" '''
            cur.execute(query)
            row = cur.fetchall()
            # This query sorts the transactions in decreasing order of date and time and selects only one among them
            query2 = f'''select * from transactions where cardno="{row[0][0]}" ORDER BY date DESC,currenttime DESC LIMIT 1 '''
            cur.execute(query2)
            row2 = cur.fetchall()
            print("hello,your previous transactions is as follows:-")
            print("your card number:", row2[0][0])
            print("Whether amount was debited or credited:-", row2[0][1])
            print("Transaction amount was=", row2[0][2])
            print("Last transaction was done on date:-", row2[0][3])
            print("Transaction time was:-", row2[0][4])
            conn.commit()
            conn.close()
        else:
            print("Card Blocked. Please  visit Bank.")

    def Linked_Cards(self, userobj):
        user_id = userobj.getUserId()
        status = userobj.getStatus()
        if status == 'ACTIVE':
            decide = input("Do you want to check all the cards linked to this user id?")
            if decide == 'y' or decide == 'Y':
                conn = sqlite3.connect("ATMSYS.s3db")
                cur = conn.cursor()
                query = f'''select cardno from users where id="{user_id}" '''
                cur.execute(query)
                row = cur.fetchall()
                query2 = f'''select * from linkedcards where cardno="{row[0][0]}" '''
                cur.execute(query2)
                row2 = cur.fetchall()
                print("CARD NO        CARD TYPE          LINKED CARD")
                for i in range(0, len(row2)):
                    print(row2[i][0], "       ", row2[i][1], "           ", row2[i][2])
                conn.commit()
                conn.close()
                print()
            else:
                print("----------------------------------------------------------------------------------")
                print("SORRY YOU DO NOT HAVE ANY CARDS LINKED")
        else:
            print("Card is Blocked. Please Visit Bank.")

if __name__ == "__main__":
    # transactions obj
    withdraw = withdraw()
    Deposit = Deposit()
    Transfer = Transfer_money()
    # settings obj
    Blockedcards = BlockedCards()
    Card_Limit = Card_Limit()
    CardPin = CardPin()
    # transaction details obj
    Transaction_details = Transaction_details()
    Feature = Feature(withdraw, Deposit, Transfer, Card_Limit, Blockedcards, CardPin, Transaction_details)
    Display = Display()
    Validation = Validation()
    ATM = ATM(Display, Validation, Feature)
    ATM.run()
