from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from chat.views import redirect_to_chat

urlpatterns = [
    path('', redirect_to_chat),
    path('auth/', include('auth.urls')),
    path('chat/', include('chat.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
