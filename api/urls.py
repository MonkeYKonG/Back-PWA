from django.urls import path
from push_notifications.api.rest_framework import GCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, SoundViewSet, AlbumViewSet, PlaylistViewSet, GetProfile, MusicStyleViewSet, \
    ArtistViewSet, UpdateProfilePicture

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'sounds', SoundViewSet, basename='sound')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'artists', ArtistViewSet, basename='artist')
router.register(r'playlists', PlaylistViewSet, basename='playlist')
router.register(r'styles', MusicStyleViewSet, basename='style')
router.register(r'device', GCMDeviceAuthorizedViewSet)

urlpatterns = router.urls + [
    path('profile/', GetProfile.as_view()),
    path('upload-profile-picture/', UpdateProfilePicture.as_view())
]
