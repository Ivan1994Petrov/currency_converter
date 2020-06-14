from django.views import View
from django.views.generic import ListView
from django.http import JsonResponse
from django.shortcuts import render
from django.core.management import call_command

from core.models import CurrencyPair
from core.forms import CalculatorForm


class CurrencyPairsList(ListView):
    """This view handles homepage with all listed currency pairs."""
    context_object_name = 'currency_pairs'
    queryset = CurrencyPair.objects.all()
    template_name = 'pages/list.html'


class Calculator(View):
    """This view handles calculator page."""
    form = CalculatorForm()

    def get(self, request):
        context = {
            'form': self.form
        }

        return render(request, 'pages/calculator.html', context)


def ajax_sync_now(request):
    """
    This view is responsibly for calling the
    extract_the_current_course from the admin panel.
    """
    call_command('extract_the_current_course')
    return JsonResponse({})


def ajax_calculator(request):
    """This view handles ajax for calculator page."""
    base_currency = request.GET.get('fromCurrencyValue', None)
    quote_currency = request.GET.get('toCurrency', None)
    amount = request.GET.get('amount', None)
    try:
        currency_pair = CurrencyPair.objects.get(
            base_currency=base_currency,
            quote_currency=quote_currency,
        )
        quote = currency_pair.quote
        result = float(quote) * float(amount)

        data = {
            'result': result
        }
        return JsonResponse(data)
    except CurrencyPair.DoesNotExist:
        currency_pairs = CurrencyPair.objects.filter(
            base_currency=base_currency
        )
        result = [currency_pair.quote_currency.quote_currency for
                  currency_pair in currency_pairs]
        data = {
            'result': result
        }
        return JsonResponse(data)
