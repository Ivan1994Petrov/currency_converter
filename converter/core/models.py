from django.db import models


class CurrencyPair(models.Model):
    base_currency = models.CharField(max_length=3)
    quote_currency = models.CharField(max_length=3)

    quote = models.DecimalField(max_digits=19, decimal_places=10)

    def __str__(self):
        return f'{self.base_currency}/{self.quote_currency} - {self.quote}'