from django import forms

from core.models import BaseCurrency, QuoteCurrency, CurrencyPair


class CalculatorForm(forms.Form):
    from_currency = forms.ModelChoiceField(queryset=BaseCurrency.objects.all())
    to_currency = forms.ModelChoiceField(queryset=QuoteCurrency.objects.all())
    amount = forms.DecimalField()