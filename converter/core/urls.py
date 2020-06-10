from django.urls import path

from core.views import CurrencyPairsList


urlpatterns = [
    path('', CurrencyPairsList.as_view(), name='currency-pairs'),
]