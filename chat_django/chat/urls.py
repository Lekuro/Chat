from django.urls import path

from . import views

urlpatterns = [
    # path('login', views.login, name='login'),
    path('', views.index_view, name='index'),
    path('<int:room_id>/users/', views.invite_user, name='invite_user_endpoint'),
    path('<int:room_id>/', views.room_view, name='room_endpoint'),
]
