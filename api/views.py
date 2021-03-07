from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from api.models import User, Sound, Album, Playlist, MusicStyle
from api.serializers import UserSerializer, SoundSerializer, AlbumSerializer, PlaylistSerializer


class IsSelf(BasePermission):
    def __init__(self, verify_function):
        self._verify_function = verify_function

    def has_permission(self, request, view):
        if 'pk' not in view.kwargs or not request.user:
            return False
        return self._verify_function(request)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def _verify_self(self, request):
        return self.kwargs['pk'] == request.user.pk

    def get_permissions(self):
        perms = []
        if self.action in ('create',):
            perms = []
        elif self.action in ('update', 'partial_update', 'delete'):
            perms += [IsSelf(self._verify_self), permissions.IsAdminUser(), permissions.IsAuthenticated(), TokenHasReadWriteScope()]
        return perms


class SoundViewSet(viewsets.ModelViewSet):
    queryset = Sound.objects.all()
    serializer_class = SoundSerializer

    def _verify_self(self, request):
        return request.user.sounds.filter(pk=self.kwargs['pk']).count() == 1

    def get_permissions(self):
        perms = []
        if self.action in ('update', 'partial_update', 'delete'):
            perms += [IsSelf(self._verify_self), permissions.IsAdminUser(), permissions.IsAuthenticated(), TokenHasReadWriteScope()]
        return perms


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def _verify_self(self, request):
        return request.user.albums.filter(pk=self.kwargs['pk']).count() == 1

    def get_permissions(self):
        perms = []
        if self.action in ('update', 'partial_update', 'delete'):
            perms += [IsSelf(self._verify_self), permissions.IsAdminUser(), permissions.IsAuthenticated(), TokenHasReadWriteScope()]
        return perms


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def _verify_self(self, request):
        return request.user.playlists.filter(pk=self.kwargs['pk']).count() == 1

    def get_permissions(self):
        perms = [permissions.IsAuthenticated(), TokenHasReadWriteScope()]
        if self.action in ('update', 'partial_update', 'delete'):
            perms += [IsSelf(self._verify_self), permissions.IsAdminUser()]
        return perms


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, TokenHasReadWriteScope])
def get_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def get_styles(request):
    return Response(MusicStyle.values)
