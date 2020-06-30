from django.test import TestCase, Client
from django.urls import reverse, resolve

from core.models import BaseCurrency, QuoteCurrency, CurrencyPair
from core.views import CurrencyPairsList, Calculator, ajax_sync_now, \
    ajax_calculator
from core.forms import CalculatorForm


class TestUrls(TestCase):
    """Test all urls into urls.py."""

    def test_currency_pairs_list_url(self):
        """Test case: test currency-pairs."""
        url = reverse('currency-pairs')
        self.assertEqual(resolve(url).func.__name__,
                         CurrencyPairsList.__name__)

    def test_calculator_url(self):
        """Test case: test calculator."""
        url = reverse('calculator')
        self.assertEqual(resolve(url).func.__name__,
                         Calculator.__name__)

    def test_ajax_sync_now_url(self):
        """Test case: test ajax-sync-now."""
        url = reverse('ajax-sync-now')
        self.assertEqual(resolve(url).func, ajax_sync_now)

    def test_ajax_calculator_url(self):
        """Test case: test ajax-calculator."""
        url = reverse('ajax-calculator')
        self.assertEqual(resolve(url).func, ajax_calculator)


class TestViews(TestCase):
    """Test all views into views.py."""
    def setUp(self):
        self.client = Client()
        self.currency_pairs_url = reverse('currency-pairs')
        self.calculator_url = reverse('calculator')
        self.ajax_sync_now_url = reverse('ajax-sync-now')
        self.ajax_calculator_url = reverse('ajax-calculator')

    def test_currency_pairs_list_GET(self):
        """Test case: test CurrencyPairsList."""
        response = self.client.get(self.currency_pairs_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/list.html')

    def test_calculator_GET(self):
        """Test case: test Calculator."""
        response = self.client.get(self.calculator_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/calculator.html')

    def test_ajax_sync_now_GET(self):
        """Test case: test ajax_sync_now."""
        response = self.client.get(self.ajax_sync_now_url)

        self.assertEqual(response.status_code, 200)

    def test_ajax_calculator_GET(self):
        """Test case: test ajax_calculator."""
        response = self.client.get(self.ajax_calculator_url)

        self.assertEqual(response.status_code, 200)


class TestCalculatorForm(TestCase):
    """Test CalculatorForm."""
    def test_calculator_form_valid_data(self):
        """Test case: passing valid data into the form."""
        from_currency_obj = BaseCurrency.objects.create(
            base_currency='USD')
        to_currency_obj = QuoteCurrency.objects.create(
            quote_currency='EUR')
        form = CalculatorForm(data={
            'from_currency': from_currency_obj.pk,
            'to_currency': to_currency_obj.pk,
            'amount': 100,
        })

        self.assertTrue(form.is_valid())

    def test_calculator_form_no_data(self):
        """Test case: check the form without data."""
        form = CalculatorForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)


class TestCurrencyPairsList(TestCase):
    """Test CurrencyPairsList view."""
    def setUp(self):
        self.client = Client()
        self.currency_pairs_url = reverse('currency-pairs')

    def test_with_item_on_the_db(self):
        """Test case: check the page with one item into DB."""
        base_currency = BaseCurrency.objects.create(
            base_currency='USD')
        quote_currency = QuoteCurrency.objects.create(
            quote_currency='EUR')
        CurrencyPair.objects.create(
            base_currency=base_currency,
            quote_currency=quote_currency,
            quote=2)

        response = self.client.get(self.currency_pairs_url)

        self.assertEqual(len(response.context['currency_pairs']), 1)

    def test_with_no_items_on_the_db(self):
        """Test case: check the page without items into DB."""
        response = self.client.get(self.currency_pairs_url)

        self.assertEqual(len(response.context['currency_pairs']), 0)


class TestCalculator(TestCase):
    """Test Calculator view."""
    def setUp(self):
        self.client = Client()
        self.calculator_url = reverse('calculator')

    def test_form_instance(self):
        """Test case: check the instance of the given form."""
        form = CalculatorForm()

        response = self.client.get(self.calculator_url)

        self.assertIsInstance(response.context['form'], type(form))


class TestAjaxCalculator(TestCase):
    """Test ajax_calculator view."""
    def setUp(self):
        self.client = Client()
        self.ajax_calculator_url = reverse('ajax-calculator')

    def test_with_currency_pair_into_db(self):
        """Test case: check the output with wanted CurrencyPair."""
        base_currency = BaseCurrency.objects.create(
            base_currency='USD')
        quote_currency = QuoteCurrency.objects.create(
            quote_currency='EUR')
        CurrencyPair.objects.create(
            base_currency=base_currency,
            quote_currency=quote_currency,
            quote=2)

        response = self.client.get(self.ajax_calculator_url, data={
            'fromCurrencyValue': base_currency.pk,
            'toCurrency': quote_currency.pk,
            'amount': 2
        })

        # result must be float number from the product of quote and amount
        expected_result = {"result": 4.0}
        result = str(response.content, encoding='utf8')

        self.assertJSONEqual(result, expected_result)

    def test_without_currency_pair_into_db(self):
        """Test case: check the output without CurrencyPair into DB."""
        response = self.client.get(self.ajax_calculator_url, data={
            'fromCurrencyValue': 2,
            'toCurrency': 2,
            'amount': 2
        })
        # result must be empty list
        expected_result = {"result": []}
        result = str(response.content, encoding='utf8')

        self.assertJSONEqual(result, expected_result)

    def test_with_non_existent_currency_pair_into_db(self):
        """Test case: check the output with wrong CurrencyPair."""
        base_currency = BaseCurrency.objects.create(
            base_currency='USD')
        quote_currency = QuoteCurrency.objects.create(
            quote_currency='EUR')
        CurrencyPair.objects.create(
            base_currency=base_currency,
            quote_currency=quote_currency,
            quote=2)

        response = self.client.get(self.ajax_calculator_url, data={
            'fromCurrencyValue': base_currency.pk,
            'toCurrency': 999,
            'amount': 2
        })

        # result must be quote_currency
        expected_result = {"result": ["EUR"]}
        result = str(response.content, encoding='utf8')

        self.assertJSONEqual(result, expected_result)
