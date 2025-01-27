from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('register/',reg,name="register"),
    path('login/',log,name='login'),
    path('dashboard/',dashboard,name='dashboard'),
    path('about/',about,name='about'),
    path('payments',pay,name='pay'),
    path('heartbeat/',heartbeat, name='heartbeat'),

]