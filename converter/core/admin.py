from django.contrib import admin

from core.models import BaseCurrency, QuoteCurrency, CurrencyPair

admin.site.register(BaseCurrency)
admin.site.register(QuoteCurrency)


@admin.register(CurrencyPair)
class CurrencyPairAdmin(admin.ModelAdmin):
    """Model for CurrencyPair"""
    list_display = ('base_currency', 'quote_currency', 'quote')
    list_filter = ('base_currency', 'quote_currency')
    search_fields = ('base_currency__base_currency', 'quote_currency__quote_currency',)
    change_list_template = 'backend/changelist.html'
    list_per_page = 20
