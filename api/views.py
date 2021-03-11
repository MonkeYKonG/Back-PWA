import abc

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import permissions, viewsets, generics, mixins

from api.models import User, Sound, Album, Playlist, MusicStyle, Artist, SoundComment, PlaylistComment, UserFollowing, \
    PlaylistFollowing, SoundLike, PlaylistLike
from api.serializers import UserSerializer, SoundSerializer, AlbumSerializer, PlaylistSerializer, ArtistSerializer, \
    MusicStyleSerializer, SoundCommentSerializer, PlaylistCommentSerializer, UserFollowingSerializer, \
    PlaylistFollowingSerializer, SoundLikeSerializer, PlaylistLikeSerializer, CompleteUserSerializer


class IsSelf(permissions.BasePermission):
    def __init__(self, verify_function):
        self._verify_function = verify_function

    def has_permission(self, request, view):
        if 'pk' not in view.kwargs or not request.user:
            return False
        return self._verify_function(request)


class CreateDestroyViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass


class CreateUpdateDestroyViewSet(mixins.UpdateModelMixin, CreateDestroyViewSet):
    pass


class ProtectedManagementViewSet(viewsets.ModelViewSet):
    @abc.abstractmethod
    def _verify_self(self, request):
        raise NotImplementedError('_verify_self must be defined on sub classes')

    def get_permissions(self):
        perms = super().get_permissions()
        if self.action in ('update', 'partial_update', 'delete'):
            perms = [IsSelf(self._verify_self), permissions.IsAdminUser()]
        return perms


class UserViewSet(ProtectedManagementViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def _verify_self(self, request):
        return self.kwargs['pk'] == request.user.pk

    def get_permissions(self):
        if self.action in ('create',):
            return []
        return super().get_permissions()


class SoundViewSet(ProtectedManagementViewSet):
    queryset = Sound.objects.all()
    serializer_class = SoundSerializer

    def _verify_self(self, request):
        return request.user.sounds.filter(pk=self.kwargs['pk']).exists()

    def get_permissions(self):
        perms = []
        if self.action in ('update', 'partial_update', 'delete'):
            perms += [IsSelf(self._verify_self), permissions.IsAdminUser(), permissions.IsAuthenticated(),
                      TokenHasReadWriteScope()]
        return perms


class AlbumViewSet(CreateUpdateDestroyViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class ArtistViewSet(CreateUpdateDestroyViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class PlaylistViewSet(ProtectedManagementViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def _verify_self(self, request):
        return request.user.playlists.filter(pk=self.kwargs['pk']).exists()


class GetProfile(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = CompleteUserSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def retrieve(self, request, *args, **kwargs):
        self.kwargs['pk'] = request.user.pk
        return super().retrieve(request, *args, **kwargs)


class MusicStyleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MusicStyle.objects.all()
    serializer_class = MusicStyleSerializer
    permission_classes = []


class SoundCommentViewSet(CreateUpdateDestroyViewSet):
    queryset = SoundComment.objects.all()
    serializer_class = SoundCommentSerializer


class PlaylistCommentViewSet(CreateUpdateDestroyViewSet):
    queryset = PlaylistComment.objects.all()
    serializer_class = PlaylistCommentSerializer


class UserFollowingViewSet(CreateDestroyViewSet):
    queryset = UserFollowing.objects.all()
    serializer_class = UserFollowingSerializer


class PlaylistFollowingViewSet(CreateDestroyViewSet):
    queryset = PlaylistFollowing.objects.all()
    serializer_class = PlaylistFollowingSerializer


class SoundLikeViewSet(CreateDestroyViewSet):
    queryset = SoundLike.objects.all()
    serializer_class = SoundLikeSerializer


class PlaylistLikeViewSet(CreateDestroyViewSet):
    queryset = PlaylistLike.objects.all()
    serializer_class = PlaylistLikeSerializer
