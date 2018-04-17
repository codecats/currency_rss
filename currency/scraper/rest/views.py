from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from scraper.models import ScrapedCurrency
from scraper.rest.serializers import ScrapedCurrencySerializer


@api_view()
def hello(request):
    return Response({'hel': 'ht'})


class ScrapedCurrencyViewSet(ReadOnlyModelViewSet):
    serializer_class = ScrapedCurrencySerializer
    queryset = ScrapedCurrency.objects.all()
