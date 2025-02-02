from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',home,name='home'),
    path('register/',reg,name="register"),
    path('login/',log,name='login'),
    path('dashboard/',dashboard,name='dashboard'),
    path('about/',about,name='about'),
    path('payments',pay,name='pay'),
    path('heartbeat/',heartbeat, name='heartbeat'),
    path('otp/', otp, name='otp'),
    path('profile/',stdprofile, name='profile')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)