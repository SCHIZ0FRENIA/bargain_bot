from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('telegram_bot.urls')),
    path('health/', lambda request: HttpResponse('ok')),
]
