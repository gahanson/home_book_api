from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register(r'book', BookViewSet)

urlpatterns = [
 path('', include(router.urls)),
 path('settings/', settings, name='settings'),
 path('refresh/', refresh, name='refresh'),
]
