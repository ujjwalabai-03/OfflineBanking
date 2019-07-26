from models import Customer, Statement
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
                     os_balance=init_bal)
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


def deposit(user):
    deposit_am = float(input("Amount to be deposited: "))
    user.balance += deposit_am
    user.save()
    state = Statement.create(ac_no=user.acc_num,
                             credit=deposit_am,
                             debit=0,
                             timestamp=datetime.now(),
                             os_balance=user.balance)


def withdraw(user):
    while True:
        withdraw_am = float(input("Amount to be withdrawn: "))
        if withdraw_am > user.balance:
            print(
                f"Not enough balance. Maximum amount is {user.balance}")
        else:
            break
    user.balance -= withdraw_am
    state = Statement.create(ac_no=user.acc_num,
                             credit=0,
                             debit=withdraw_am,
                             timestamp=datetime.now(),
                             os_balance=user.balance)


def gen_statement(user):
    print(f"Name: {user.full_name}")
    print(f"Account Number: {user.acc_num} \n")
    entries = Statement.select().where(Statement.ac_no == user.acc_num)
    table = PrettyTable(["Date and Time", "Credit", "Debit", "Balance"])
    for entry in entries:
        table.add_row([str(entry.timestamp)[:19], entry.credit,
                       entry.debit, entry.os_balance])
    print(table)
    dummy = input()
    print("Press any key")
