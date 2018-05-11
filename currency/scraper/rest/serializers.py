from rest_framework.serializers import ModelSerializer

from scraper.models import ScrapedCurrency


class ScrapedCurrencySerializer(ModelSerializer):
    class Meta(object):
        model = ScrapedCurrency
        fields = '__all__'
