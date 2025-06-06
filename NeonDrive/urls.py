from django.contrib import admin
from django.urls import path, include
from main.views import home, feedback, register

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # Подключаем main.urls в корень
]