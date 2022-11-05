from knox import views as knox_views
from django.urls import path, include
from . import views

urlpatterns = [
    # path('auth/', include('knox.urls')),
    path('token-exchange/',  views.token_exchange, name='token-exchange'),
    path('public-token/', views.get_public_token, name='public-token'),
    path('transactions/all/', views.get_transactions, name='all-transcations'),
    path('accounts/', views.get_accounts, name='accounts')

    
]