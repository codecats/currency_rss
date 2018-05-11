from django.conf.urls import url, include
from rest_framework import routers

from scraper.rest.views import ScrapedCurrencyViewSet

router = routers.DefaultRouter()

router.register(r'api', ScrapedCurrencyViewSet, 'api')

urlpatterns = [
    url(r'^', include(router.urls)),
]
