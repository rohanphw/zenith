from tortoise import fields
from dipdup.models import Model


class User(Model):
    address = fields.CharField(52, pk=True)
    balance = fields.CharField(max_length=32)


class IncreasePosition(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='increase_positions')
    amount = fields.CharField(max_length=32)


class DecreasePosition(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='decrease_positions')
    amount = fields.CharField(max_length=32)


class ClosePosition(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='close_positions')


class AddMargin(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='add_margins')
    amount = fields.CharField(max_length=32)


class RemoveMargin(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='remove_margins')
    amount = fields.CharField(max_length=32)


class MarkedPrice(Model):
    id = fields.IntField(pk=True)
    price = fields.CharField(max_length=32)
    timestamp = fields.DatetimeField(auto_now_add=True)