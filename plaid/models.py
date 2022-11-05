from django.db import models
from django.contrib.auth.models import User


class TokenExchangeModel(models.Model):
    name = 'token_exchange'
    class Meta:
        app_label = 'plaid'

    access_token = models.CharField(max_length=300)
    public_token = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class AccountModel(models.Model):
    name = 'accounts'
    class Meta:
        app_label = 'plaid'
    account_id = models.CharField(max_length=300, unique=True)
    balance_available =  models.IntegerField()
    balance_current =  models.IntegerField()
    balance_currency = models.CharField(max_length=30, unique=True)
    account_official_name = models.CharField(max_length=300, unique=True)
    account_type = models.CharField(max_length=300, unique=True)
    account_subtype = models.CharField(max_length=300, unique=True)


class TransactionModel(models.Model):
    name = 'transcations'
    class Meta:
        app_label = 'plaid'
    transaction_id = models.CharField(max_length=100)
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField()
    name = models.CharField(max_length=100),
    pending = models.BooleanField()

class LogModel(models.Model):
    name = 'logs'
    class Meta:
        app_label = 'plaid'
    api = models.CharField(max_length=200)
    date = models.DateTimeField(verbose_name='date_log', auto_now_add=True)