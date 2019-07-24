from models import Customer, Statement
from random import randrange
from datetime import datetime


def register():
    name = input("Enter full name: ")
    pin = int(input("Enter PIN: "))
    while True:
        temp_acc = randrange(10000, 99999)
        acc = Customer.select().where(Customer.acc_num == temp_acc)
        if acc.exists():
            continue
        else:
            gen_acc = temp_acc
            break
    init_bal = float(input("Enter initial balance: "))
    Customer.create(full_name=name, pin=pin, acc_num=gen_acc, balance=init_bal)


def login():
    while True:
        acc_no = input("Enter the account number: ")
        acc = Customer.select().where(Customer.acc_num == acc_no)
        if not acc.exists():
            print("Enter valid account number!")
        else:
            break
    count = 0
    user = Customer.select().where(Customer.acc_num == acc_no)
    pin_acc = int(user.get().pin)
    while count < 3:
        pin = int(input("Enter Pin: "))
        if pin == pin_acc:
            break
        else:
            count += 1
            print(f"Wrong password! You have {3-count} tries left")
    if count == 3:
        print("Access locked. Try Later")
        exit()
    print("Logged in successfully!")
    return (user, 1)


def deposit(user):
    deposit = float(input("Amount to be deposited: "))
    new_bal = user.balance + deposit
    upd_user = Customer.update(Customer.balance=new_bal).where(Customer.acc_num == user.acc_num)
    upd_user.execute()
    state = Statement.create(Statement.ac_no=user.acc_num,
                             Statement.credit=deposit,
                             Statement.debit=0,
                             Statement.timestamp=datetime.now(),
                             Statement.balance=new_bal)
    print("Deposit successful!")


def withdraw(user):
    while True:
        withdraw = float(input("Amount to be withdrawn: "))
        temp = Customer.select().where(Customer.acc_num == user.acc_num)
        if withdraw > temp.get().balance:
            print(
                f"Not enough balance. Maximum amount is {temp.get().balance}")
        else:
            break
    new_bal = user.balance - withdraw
    upd_user = Customer.update(Customer.balance=new_bal).where(Customer.acc_num == user.acc_num)
    upd_user.execute()
    state = Statement.create(Statement.ac_no=user.acc_num,
                             Statement.credit=0,
                             Statement.debit=withdraw,
                             Statement.timestamp=datetime.now(),
                             Statement.balance=new_bal)
    print("Withdrawal successful!")


def gen_statement():
    entries = Statement.select().where(Statement.ac_no == user.acc_num)
    for entry in entries:
        print(f"{entry[0]:<9}{entry[1]:<15}{entry[2]:<15}{entry[3]:<20}{entry[4]:<15")
