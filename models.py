from peewee import *
db = SqliteDatabase('banking.db')


class Customer(Model):
    full_name = CharField()
    pin = IntegerField()
    acc_num = IntegerField()

    class Meta:
        database = db  # This model uses the "journal.db" database


class Statement(Model):
    ac_no = ForeignKeyField(customer, backref='customer')
    credit = FloatField()
    debit = FloatField()
    timestamp = DateTimeField()
    balance = FloatField()

    class Meta:
        database = db


if __name__ == "__main__":
    db.connect()
    db.create_tables([Customer, Statement])
