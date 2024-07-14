from django.urls import path
from . import views

urlpatterns = [
    path('import/', views.import_accounts, name='import_accounts'),
    path('accounts/', views.list_accounts, name='list_accounts'),
    path('accounts/<str:account_number>/', views.account_detail, name='account_detail'),
    path('transfer/', views.transfer_funds, name='transfer_funds'),
]
