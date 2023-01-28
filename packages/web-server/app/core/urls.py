from core.views import GalleryView
from django.urls import path

urlpatterns = [
    path('gallery', GalleryView.as_view(), name='gallery'),
]
