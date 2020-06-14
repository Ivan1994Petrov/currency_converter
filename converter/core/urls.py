from django.urls import path

from core.views import CurrencyPairsList, Calculator, ajax_sync_now

urlpatterns = [
    path('', CurrencyPairsList.as_view(), name='currency-pairs'),
    path('calculator/', Calculator.as_view(), name='calculator'),
    path('ajax/sync-now/', ajax_sync_now, name='ajax-sync-now')
]
