from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from core.models import BaseCurrency, QuoteCurrency, CurrencyPair
from core.forms import CalculatorForm

class CurrencyPairsList(ListView):
    context_object_name = 'currency_pairs'
    queryset = CurrencyPair.objects.all()
    template_name = 'pages/list.html'


class Calculator(View):
    form = CalculatorForm()
    def get(self, request):

        data = CurrencyPair.objects.all()
        context = {
            # I need to rename the key and the value
            'test': data,
            'form': self.form
        }

        return render(request, 'pages/calculator.html', context)

    def post(self, request):
        post_data = request.POST
        print(post_data)
        from_currency = post_data.get('from_currency')
        to_currency = post_data.get('to_currency')
        amount = post_data.get('amount')

        try:
            item = CurrencyPair.objects.get(
                base_currency=from_currency,
                quote_currency=to_currency)
            quote = item.quote
            result = float(amount) * float(quote)
            return HttpResponse(f'{amount}*{quote}={result}')
        except ObjectDoesNotExist:
            # if I don't have this pair into the DB

            # here I need to filter only for base_currency and to render that for this currency we have only ...

            items = CurrencyPair.objects.filter(
                base_currency=from_currency)
            base_currency_obj = BaseCurrency.objects.get(pk=from_currency)
            # todo change the name of template
            context = {
                # I need to rename the key and the value
                'base_currency_obj': base_currency_obj,
                'items': items,
            }
            return render(request, 'pages/missing_pair.html', context)
