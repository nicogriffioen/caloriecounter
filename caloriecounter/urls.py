"""caloriecounter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from caloriecounter.food.api.urls import urlpatterns as food_api_urls
from caloriecounter.diary.api.urls import urlpatterns as diary_api_urls
from caloriecounter.voice.api.urls import urlpatterns as voice_api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(food_api_urls +
                         diary_api_urls +
                         voice_api_urls)),
]
