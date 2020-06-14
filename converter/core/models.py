from django.db import models


class BaseCurrency(models.Model):
    base_currency = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return f'{self.base_currency}'


class QuoteCurrency(models.Model):
    quote_currency = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return f'{self.quote_currency}'


class CurrencyPair(models.Model):
    base_currency = models.ForeignKey(BaseCurrency,
                                      on_delete=models.CASCADE)
    quote_currency = models.ForeignKey(QuoteCurrency,
                                       on_delete=models.CASCADE)
    quote = models.DecimalField(max_digits=19, decimal_places=6)

    def __str__(self):
        return f'{self.base_currency} - {self.quote_currency} - {self.quote}'
