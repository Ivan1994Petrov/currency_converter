from django.urls import path

from core.views import CurrencyPairsList, Calculator


urlpatterns = [
    path('', CurrencyPairsList.as_view(), name='currency-pairs'),
    path('calculator/', Calculator.as_view(), name='calculator'),
]