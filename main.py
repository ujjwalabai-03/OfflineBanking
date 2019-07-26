from app import *
import os
log = 0
iv_flag = 0
success_str = ''
while True:
    os.system("clear")
    if success_str != '':
        print(success_str)
        success_str = ''
    else:
        print("Welcome!")
    print("Choose an option")
    print("1.Login to Account")
    print("2.Register New User")
    print("Any other key to exit")
    choice = input(">>> ")
    if choice == "1":
        os.system("clear")
        (user, log) = login()
        while log == 1:
            os.system("clear")
            if user:
                if success_str != '':
                    print(success_str)
                    success_str = ''
                print("Choose an option")
                print("1.Make Deposit ")
                print("2.Withdraw from Account")
                print("3.See MiniStatement")
                print("4.Logout")
                if iv_flag == 1:
                    print("Invalid input! Enter again")
                iv_flag = 0
                choice = input(">>> ")
                if choice == "1":
                    deposit(user)
                    success_str = "Deposit successful"
                elif choice == "2":
                    withdraw(user)
                    success_str = "Withdrawal successful"
                elif choice == "3":
                    os.system("clear")
                    gen_statement(user)
                elif choice == "4":
                    log = 0
                else:
                    iv_flag == 1
    elif choice == "2":
        os.system("clear")
        print("Registration \n \n")
        user = register()
        success_str = "Registration successful"
    else:
        exit()
