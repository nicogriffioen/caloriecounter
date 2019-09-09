from django.urls import include, path
from rest_framework import routers

from caloriecounter.diary.api import views

router = routers.DefaultRouter()
router.register(r'diary_entry', views.DiaryEntryViewSet, base_name='diary_entry')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]