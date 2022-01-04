from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import CategoriesListView, PostViewSet

router = DefaultRouter()
router.register('post', PostViewSet)


urlpatterns = [
    path('categories', CategoriesListView.as_view()),
    path('', include(router.urls))

]