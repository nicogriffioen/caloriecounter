from django.urls import include, path
from rest_framework import routers

from caloriecounter.voice.api import views

router = routers.DefaultRouter()
router.register(r'voice_session', views.VoiceSessionViewSet, basename='voice_session')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]