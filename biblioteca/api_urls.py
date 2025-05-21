from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import LibroViewSet

router = DefaultRouter()
router.register(r'libros', LibroViewSet, basename='libro')

urlpatterns = router.urls
