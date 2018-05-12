from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.test import APIClient, APITestCase

from scraper.models import ScrapedCurrency


class RestScrapedCurrencyTest(APITestCase):
    URL = reverse('api-list')
    def test_empty_data(self):

        response = self.client.get(self.URL, {}, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_not_allowed_methods(self):
        methods = ['post', 'patch', 'put', 'delete']
        for m in methods:
            response = getattr(self.client, m)(self.URL, {}, format='json')
            self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_scraped_data(self):
        ScrapedCurrency.objects.bulk_create([ScrapedCurrency(country='usd', value=i) for i in range(10)])
        response = self.client.get(self.URL, {}, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 10)
        ScrapedCurrency.objects.all().delete()