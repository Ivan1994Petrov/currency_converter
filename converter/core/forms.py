from django import forms

from core.models import BaseCurrency, QuoteCurrency


class CalculatorForm(forms.Form):
    """Form for calculator page"""
    from_currency = forms.ModelChoiceField(
        queryset=BaseCurrency.objects.all(), label='Валута от')
    to_currency = forms.ModelChoiceField(
        queryset=QuoteCurrency.objects.all(), label='Валута в')
    amount = forms.DecimalField(label='Сума')
