from django.views import View
from django.views.generic import ListView
from django.http import JsonResponse
from django.shortcuts import render
from django.core.management import call_command

from core.models import BaseCurrency, QuoteCurrency, CurrencyPair
from core.forms import CalculatorForm


class CurrencyPairsList(ListView):
    context_object_name = 'currency_pairs'
    queryset = CurrencyPair.objects.all()
    template_name = 'pages/list.html'


class Calculator(View):
    form = CalculatorForm()

    def get(self, request):
        context = {
            'form': self.form
        }

        return render(request, 'pages/calculator.html', context)


def ajax_sync_now(request):
    call_command('extract_the_current_course')
    return JsonResponse({})


def ajax_calculator(request):
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
    except:
        currency_pairs = CurrencyPair.objects.filter(
            base_currency=base_currency
        )
        result = [currency_pair.quote_currency.quote_currency for
                  currency_pair in currency_pairs]
        data = {
            'result': result
        }
        return JsonResponse(data)
