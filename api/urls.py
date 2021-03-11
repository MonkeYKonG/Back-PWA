from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, SoundViewSet, AlbumViewSet, PlaylistViewSet, GetProfile, MusicStyleViewSet, \
    SoundCommentViewSet, PlaylistCommentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'sounds', SoundViewSet, basename='sound')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'playlists', PlaylistViewSet, basename='playlist')
router.register(r'styles', MusicStyleViewSet, basename='style')
router.register(r'sound-comments', SoundCommentViewSet, basename='sound-comment')
router.register(r'playlist-comments', PlaylistCommentViewSet, basename='playlist-comment')

urlpatterns = router.urls + [
    path('profile/', GetProfile.as_view()),
]
