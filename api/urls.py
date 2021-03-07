from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, SoundViewSet, AlbumViewSet, PlaylistViewSet, get_profile, get_styles

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'sounds', SoundViewSet, basename='sound')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'playlists', PlaylistViewSet, basename='playlist')

urlpatterns = router.urls + [
    path('profile/', get_profile),
    path('styles/', get_styles),
]
