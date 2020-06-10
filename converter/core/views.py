from django.views.generic import ListView

from core.models import CurrencyPair


class CurrencyPairsList(ListView):
    context_object_name = 'currency_pairs'
    queryset = CurrencyPair.objects.all()
    template_name = 'pages/list.html'
