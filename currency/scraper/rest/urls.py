from django.conf.urls import url, include
from rest_framework import routers
import views

router = routers.DefaultRouter()

router.register(r'api', views.ScrapedCurrencyViewSet, 'api')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^hel', views.hello),
]