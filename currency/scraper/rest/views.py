from rest_framework.viewsets import ReadOnlyModelViewSet

from scraper.models import ScrapedCurrency
from scraper.rest.serializers import ScrapedCurrencySerializer


class ScrapedCurrencyViewSet(ReadOnlyModelViewSet):
    serializer_class = ScrapedCurrencySerializer
    queryset = ScrapedCurrency.objects.all()
