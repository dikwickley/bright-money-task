from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import permissions, generics
from rest_framework.views import APIView
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import requests
import json
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from plaid.models import TokenExchangeModel
from plaid.logger import logger
from plaid.tasks import shared_fetch_transactions

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_public_token(request: Request):
    url = f'{settings.PLAID_BASE}/sandbox/public_token/create'
    payload = {
        "client_id": settings.PLAID_CLIENT_ID,
        "secret": settings.PLAID_SECRET,
        "institution_id":"ins_3",
        "initial_products":["transactions"],
    }
    headers = {
    'Content-Type': "application/json",
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    response_data = response.json()
    return Response({
        "success": True,
        "public_token" : response_data["public_token"]
    })


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def token_exchange(request: Request):
    
    logger("token exchange api")

    public_token = request.data["public_token"]
    url = f'{settings.PLAID_BASE}/item/public_token/exchange'
    payload = {
        "client_id": settings.PLAID_CLIENT_ID,
        "secret": settings.PLAID_SECRET,
        "public_token":public_token,
    }
    headers = {
    'Content-Type': "application/json",
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    response_data = response.json()

    print(response_data)

    
    token_exchange_obj = TokenExchangeModel(access_token = response_data["access_token"],
        public_token = public_token,
        user = request.user
        )

    token_exchange_obj.save()

    

    access_token = response_data["access_token"]

    shared_fetch_transactions.delay(access_token)

    return Response({
        "success": True,
        "access_token" : response_data["access_token"],
        "item_id" : response_data["item_id"]
    }) 
    
def fetch_transactions(access_token: str):
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
    return response_data

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_accounts(request: Request):
    access_token = request.data["access_token"]
    response_data = fetch_transactions(access_token)
    return Response({
        "success": True,
        "accounts": response_data["accounts"]
    })

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_transactions(request: Request):
    access_token = request.data["access_token"]
    response_data = fetch_transactions(access_token)

    return Response({
        "success": True,
        "transactions": response_data["transactions"]
    })


