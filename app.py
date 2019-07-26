from models import Customer, Statement, Transactions
from random import randrange
from datetime import datetime
from prettytable import PrettyTable
import os


def register():
    name = input("Enter full name: ")
    pin = int(input("Enter a four digit PIN: "))
    while True:
        temp_acc = randrange(10000, 99999)
        acc = Customer.select().where(Customer.acc_num == temp_acc)
        if acc.exists():
            continue
        else:
            gen_acc = temp_acc
            break
    init_bal = float(input("Enter initial balance: "))
    print(f"Your account number is: {gen_acc}")
    Customer.create(full_name=name, pin=pin, acc_num=gen_acc, balance=init_bal)
    Statement.create(ac_no=gen_acc,
                     credit=init_bal,
                     debit=0,
                     timestamp=datetime.now(),
                     os_balance=init_bal,
                     description="Opening balance")
    print("Press any key")
    dummy = input()


def login():
    flag = 0
    while True:
        replace_str = ''
        if flag == 0:
            pass
        else:
            replace_str = "valid "
        acc_no = input(f"Enter {replace_str}account number: ")
        acc = Customer.select().where(Customer.acc_num == acc_no)
        if not acc.exists():
            flag = 1
            os.system("clear")
        else:
            flag = 0
            break
    count = 0
    user = Customer.select().where(Customer.acc_num == acc_no)
    pin_acc = int(user.get().pin)
    while count < 3:
        if flag == 1:
            os.system("clear")
            print(f"Wrong password! You have {3-count} tries left")
        pin = int(input("Enter Pin: "))
        if pin == pin_acc:
            break
        else:
            count += 1
            flag = 1
    if count == 3:
        os.system("clear")
        print("Access locked. Try Later")
        print("Press any key to exit")
        dummy = input()
        exit()
    return (user.get(), 1)


def deposit(user, descript):
    deposit_am = float(input("Amount: "))
    user.balance += deposit_am
    user.save()
    state = Statement.create(ac_no=user.acc_num,
                             credit=deposit_am,
                             debit=0,
                             timestamp=datetime.now(),
                             os_balance=user.balance,
                             description=descript)


def withdraw(user, descript):
    flag = 0
    while True:
        os.system("clear")
        if flag == 1:
            print(f"Not enough balance. Maximum amount is {user.balance}")
        withdraw_am = float(input("Amount: "))
        if withdraw_am > user.balance:
            flag = 1
        else:
            break
    user.balance -= withdraw_am
    state = Statement.create(ac_no=user.acc_num,
                             credit=0,
                             debit=withdraw_am,
                             timestamp=datetime.now(),
                             os_balance=user.balance,
                             description=descript)


def gen_statement(user):
    print(f"Name: {user.full_name}")
    print(f"Account Number: {user.acc_num} \n")
    entries = Statement.select().where(Statement.ac_no == user.acc_num)
    table = PrettyTable(
        ["Date and Time", "Credit", "Debit", "Balance", "Description"])
    for entry in entries:
        table.add_row([str(entry.timestamp)[:19], entry.credit,
                       entry.debit, entry.os_balance, entry.description])
    print(table)
    dummy = input()
    print("Press any key")


def transaction(user):
    flag = 0
    success_msg = ''
    while True:
        os.system("clear")
        if success_msg != '':
            print(success_msg)
            success_msg = ''
        num_str = ''
        transout = Transactions.select().where(
            (Transactions.sender_acc == user.acc_num) &
            (Transactions.done == 0))
        req_count = transout.count()
        if req_count > 0:
            num_str = f"({req_count})"
        if flag == 1:
            print("Invalid input !")
            flag = 0
        print("Transactions Menu")
        print("1.Transfer")
        print("2.Request transfer")
        print(f"3.Requests{num_str}")
        print("4.Refresh")
        print("5.Back to main menu")
        choice = input(">>>")
        if choice == "1":
            transfer(user)
            success_msg = "Transfer successful!"
        elif choice == "2":
            request(user)
            success_msg = "Request sent!"
        elif choice == "3":
            comp_request(user)
            success_msg = "Request completed!"
        elif choice == "4":
            continue
        elif choice == "5":
            break
        else:
            flag = 1


def transfer(user):
    flag = 0
    while True:
        os.system("clear")
        if flag == 2:
            print("Cannot transfer money to self")
            flag = 1
        if flag == 0:
            rec_acc = int(input("Enter the account number of recepient: "))
        if flag == 1:
            rec_acc = int(input("Enter a valid account number: "))
        user_check = Customer.select().where(Customer.acc_num == rec_acc)
        if user_check.exists():
            if user_check.get().acc_num == user.acc_num:
                flag = 2
            else:
                break
        else:
            flag = 1
    withdraw(user, f"Tsfr to Acc.no {rec_acc}")
    deposit(user_check.get(), f"Tsfr by Acc.no {user.acc_num}")
