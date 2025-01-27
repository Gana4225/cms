from django.urls import path
from .views import gana

app_name = 'payments'

urlpatterns = [
    path('tt/',gana,name='home1'),
]