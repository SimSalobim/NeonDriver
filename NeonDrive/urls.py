"""
URL configuration for NeonDrive project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from main.views import toggle_like, get_likes, CustomLoginView, CustomLogoutView, home, feedback, register


class Сars:
    pass


urlpatterns = [
    path('', home, name='home'),
    path('toggle-like/<int:car_id>/', toggle_like, name='toggle_like'),
    path('get-likes/<int:car_id>/', get_likes, name='get_likes'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('cars/', Сars, name='cars'),
    path('register/', register, name='register'),
    path('feedback/', feedback, name='feedback'),
    path('toggle-like/<int:car_id>/', toggle_like, name='toggle_like'),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]
