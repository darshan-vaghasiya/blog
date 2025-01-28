from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import PostViewSet

router = SimpleRouter()
router.register(r'', PostViewSet, basename='all_post')

app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),
]
