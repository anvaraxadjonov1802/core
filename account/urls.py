from django.urls import path
from .views import *


urlpatterns = [
    path("login/", log_in, name='log_in'),
    path("register/", register, name='register'),
    path('logout/', log_out, name='log_out'),
]