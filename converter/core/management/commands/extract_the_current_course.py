from django.core.management.base import BaseCommand
from django.db import IntegrityError

import requests
from bs4 import BeautifulSoup

from core.models import BaseCurrency, QuoteCurrency, CurrencyPair


class Command(BaseCommand):
    help = 'Management command for extracting the' \
           ' current exchange rate from the BNB website'

    def handle(self, *args, **options):
        """Get data from bnb.bg."""

        url = 'http://bnb.bg/Statistics/StExternalSector/' \
              'StExchangeRates/StERForeignCurrencies/index.htm'

        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('form', attrs={'class': 'from_to_date'})

        for row in table.find_all('tr'):
            code_and_values = row.find_all('td',
                                           attrs={'class': 'center', })
            units = row.find_all('td', attrs={'class': 'right'})
            try:
                base_currency = code_and_values[0].text
                unit = int(units[0].text)
                quote_currency = 'BGN'
                quote = round(float(code_and_values[1].text) / unit, 6)

                self.update_database(
                    base_currency,
                    quote_currency,
                    quote)

                # reverse quote and base currencies
                quote_currency = base_currency
                base_currency = 'BGN'
                quote = float(code_and_values[2].text)

                self.update_database(
                    base_currency,
                    quote_currency,
                    quote)

            except Exception:
                pass

    def update_database(self,
                        base_currency,
                        quote_currency,
                        quote):
        """
        Check and create/update BaseCurrency,
        QuoteCurrency and CurrencyPair.
        """
        try:
            BaseCurrency.objects.create(
                base_currency=base_currency
            )
        except IntegrityError:
            pass
        try:
            QuoteCurrency.objects.create(
                quote_currency=quote_currency
            )
        except IntegrityError:
            pass
        base_currency_obj_from_db = BaseCurrency.objects.get(
            base_currency=base_currency
        )

        quote_currency_obj_from_db = QuoteCurrency.objects.get(
            quote_currency=quote_currency
        )
        try:
            currency_pair_obj = CurrencyPair.objects.get(
                base_currency=base_currency_obj_from_db,
                quote_currency=quote_currency_obj_from_db,
            )
            currency_pair_obj.delete()
        except CurrencyPair.DoesNotExist:
            pass

        CurrencyPair.objects.create(
            base_currency=base_currency_obj_from_db,
            quote_currency=quote_currency_obj_from_db,
            quote=quote
        )
