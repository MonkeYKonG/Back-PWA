from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, SoundViewSet, AlbumViewSet, PlaylistViewSet, GetProfile, MusicStyleViewSet, \
    SoundCommentViewSet, PlaylistCommentViewSet, UserFollowingViewSet, PlaylistFollowingViewSet, SoundLikeViewSet, \
    PlaylistLikeViewSet, ArtistViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'sounds', SoundViewSet, basename='sound')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'artists', ArtistViewSet, basename='artist')
router.register(r'playlists', PlaylistViewSet, basename='playlist')
router.register(r'styles', MusicStyleViewSet, basename='style')
router.register(r'sound-comments', SoundCommentViewSet, basename='sound-comment')
router.register(r'playlist-comments', PlaylistCommentViewSet, basename='playlist-comment')
router.register(r'user-follow', UserFollowingViewSet, basename='user-follow')
router.register(r'playlist-follow', PlaylistFollowingViewSet, basename='playlist-follow')
router.register(r'sound-like', SoundLikeViewSet, basename='sound-like')
router.register(r'playlist-like', PlaylistLikeViewSet, basename='playlist-like')

urlpatterns = router.urls + [
    path('profile/', GetProfile.as_view()),
]
