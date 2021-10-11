from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_view, name='start_endpoint'),
    path('login', views.login_view, name='login_endpoint'),
    path('registration', views.registration_view, name='registration_endpoint'),
]
