from celery import shared_task
from django.conf import settings
import requests
import json

@shared_task
def token_exchange(public_token: str):
    pass

@shared_task
def shared_fetch_transactions(access_token: str):
    url = f'{settings.PLAID_BASE}/transactions/get'
    payload = {
        "client_id": settings.PLAID_CLIENT_ID,
        "secret": settings.PLAID_SECRET,
        "access_token": access_token,
		"start_date":"2022-01-01",
		"end_date":"2022-11-05"
    }
    headers = {
    'Content-Type': "application/json",
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    response_data = response.json()

    accounts = response_data["accounts"]
    transactions =  response_data["transactions"]

    #save this data in db


    