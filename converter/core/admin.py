from django.contrib import admin

from core.models import BaseCurrency, QuoteCurrency, CurrencyPair

admin.site.register(BaseCurrency)
admin.site.register(QuoteCurrency)


@admin.register(CurrencyPair)
class CurrencyPairAdmin(admin.ModelAdmin):
    list_display = ('base_currency', 'quote_currency', 'quote')
    list_filter = (('base_currency'), ('quote_currency'))
    change_list_template = 'backend/changelist.html'
    list_per_page = 20
