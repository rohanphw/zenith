from tortoise import fields
from dipdup.models import Model


class User(Model):
    address = fields.CharField(36, pk=True)
    balance = fields.IntField()


class IncreasePosition(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='increase_positions')
    amount = fields.IntField()


class DecreasePosition(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='decrease_positions')
    amount = fields.IntField()


class ClosePosition(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='close_positions')


class AddMargin(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='add_margins')
    amount = fields.IntField()


class RemoveMargin(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='remove_margins')
    amount = fields.IntField()
