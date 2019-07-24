from app import *
log = 0
while True:
	print("Choose an option. \n \
		1.Login to Account.\n \
		2.Register New User. \n ")				
	choice = input(" --> ")

	if choice == "1":
		(user, log) = login()
		while log = 1:
			if user :
				print("Choose an option.\n \
					1.Make Deposit.\n \
					2.Withdraw from Account.\n \
					3.See MiniStatement.\n \
					4.Logout.\n ")
				choice = input(" --> ")

				if choice == "1":
					deposit()

				elif choice == "2":
					withdraw()

				elif choice == "3":
					gen_statement()

				elif choice == "4":
					log = 0
				else:
					print("Invalid Input")				

	elif choice == "2":
		user = register()

	else :
		exit()