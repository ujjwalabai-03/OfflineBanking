from peewee import *

db = SqliteDatabase('journal.db')

class customer(Model):
	#full_name = CharField()
	full_name = CharField()
	pin = IntegerField()
	acc_num = IntegerField()

	class Meta:
		database = db # This model uses the "journal.db" database

class statement(Model):
	ac_no = ForeignKeyField(customer, backref='customer')
	credit = FloatField()
	debit = FloatField()
	timestamp = DateTimeField()
	balance = FloatField()


	class Meta:
		database = db   

if __name__ == "__main__":
	# run only when models.py is executed
	# wont run when models.py is imported
	#print("im in")
	db.connect()
	db.create_tables([User, JournalEntry])        