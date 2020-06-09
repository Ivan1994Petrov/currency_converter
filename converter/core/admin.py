from django.contrib import admin

from core.models import CurrencyPair


@admin.register(CurrencyPair)
class CurrencyPairAdmin(admin.ModelAdmin):
    list_display = ('base_currency', 'quote_currency', 'quote')
    list_filter = (('base_currency'), ('quote_currency'))
    search_fields = ('base_currency', 'quote_currency')