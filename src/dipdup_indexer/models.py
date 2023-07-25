from tortoise import fields
from dipdup.models import Model


class User(Model):
    address = fields.CharField(36, pk=True)
    balance = fields.IntField()