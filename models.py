from peewee import *
db = SqliteDatabase('Banking.db')


class Customer(Model):
    full_name = CharField()
    pin = IntegerField()
    acc_num = IntegerField()
    balance = FloatField()

    class Meta:
        database = db  # This model uses the "Banking.db" database


class Statement(Model):
    ac_no = ForeignKeyField(Customer, backref='customer')
    credit = FloatField()
    debit = FloatField()
    timestamp = TimestampField()
    os_balance = FloatField()

    class Meta:
        database = db


if __name__ == "__main__":
    db.connect()
    db.create_tables([Customer, Statement])
