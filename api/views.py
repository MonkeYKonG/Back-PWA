import abc

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import permissions, viewsets, generics, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import User, Sound, Album, Playlist, MusicStyle, Artist, SoundComment, PlaylistComment, UserFollowing, \
    PlaylistFollowing, SoundLike, PlaylistLike
from api.serializers import UserSerializer, SoundSerializer, AlbumSerializer, PlaylistSerializer, ArtistSerializer, \
    MusicStyleSerializer, SoundCommentSerializer, PlaylistCommentSerializer, UserFollowingSerializer, \
    PlaylistFollowingSerializer, SoundLikeSerializer, PlaylistLikeSerializer, CompleteUserSerializer, \
    CompleteSoundSerializer, CompletePlaylistSerializer, CompleteAlbumSerializer, CompleteArtistSerializer


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
            perms = [permissions.OR(IsSelf(self._verify_self), permissions.IsAdminUser())]
        return perms


class UserViewSet(ProtectedManagementViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def _verify_self(self, request):
        return int(self.kwargs['pk']) == int(request.user.pk)

    def get_permissions(self):
        if self.action in ('create',):
            return []
        return super().get_permissions()

    @action(methods=['post'], detail=True, serializer_class=UserFollowingSerializer)
    def follow(self, request, pk=None):
        user = self.get_object()
        serializer = UserFollowingSerializer(data=request.data, context={'request': request, 'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SoundViewSet(ProtectedManagementViewSet):
    queryset = Sound.objects.all()
    serializer_class = SoundSerializer

    def _verify_self(self, request):
        return request.user.sounds.filter(pk=self.kwargs['pk']).exists()

    def get_permissions(self):
        perms = []
        if self.action in ('update', 'partial_update', 'delete'):
            perms += [permissions.OR(IsSelf(self._verify_self), permissions.IsAdminUser())]
        if self.action == 'comment':
            return super().get_permissions()
        return perms

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompleteSoundSerializer
        return super().get_serializer_class()

    @action(methods=['POST'], detail=True, serializer_class=SoundCommentSerializer)
    def comment(self, request, pk=None):
        sound = self.get_object()
        serializer = SoundCommentSerializer(data=request.data, context={'request': request, 'sound': sound})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['post'], detail=True, serializer_class=SoundLikeSerializer)
    def like(self, request, pk=None):
        sound = self.get_object()
        serializer = SoundLikeSerializer(data=request.data, context={'request': request, 'sound': sound})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompleteAlbumSerializer
        return super().get_serializer_class()


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompleteArtistSerializer
        return super().get_serializer_class()


class PlaylistViewSet(ProtectedManagementViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def _verify_self(self, request):
        return request.user.playlists.filter(pk=self.kwargs['pk']).exists()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompletePlaylistSerializer
        return super().get_serializer_class()

    @action(methods=['POST'], detail=True, serializer_class=PlaylistCommentSerializer)
    def comment(self, request, pk=None):
        playlist = self.get_object()
        serializer = PlaylistCommentSerializer(data=request.data, context={'request': request, 'playlist': playlist})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['post'], detail=True, serializer_class=PlaylistLikeSerializer)
    def like(self, request, pk=None):
        playlist = self.get_object()
        serializer = PlaylistLikeSerializer(data=request.data, context={'request': request, 'playlist': playlist})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['post'], detail=True, serializer_class=PlaylistFollowingSerializer)
    def follow(self, request, pk=None):
        playlist = self.get_object()
        serializer = PlaylistFollowingSerializer(data=request.data, context={'request': request, 'playlist': playlist})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



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
