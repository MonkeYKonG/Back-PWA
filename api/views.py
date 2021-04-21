import abc

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import Http404
from django.conf import settings
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import permissions, viewsets, generics, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api import models
from api.models import User, Sound, Album, Playlist, MusicStyle, Artist, SoundComment, PlaylistComment, UserFollowing, \
    PlaylistFollowing, SoundLike, PlaylistLike, ProfilePicture
from api.serializers import UserSerializer, SoundSerializer, AlbumSerializer, PlaylistSerializer, ArtistSerializer, \
    MusicStyleSerializer, SoundCommentSerializer, PlaylistCommentSerializer, UserFollowingSerializer, \
    PlaylistFollowingSerializer, SoundLikeSerializer, PlaylistLikeSerializer, CompleteUserSerializer, \
    CompleteSoundSerializer, CompletePlaylistSerializer, CompleteAlbumSerializer, CompleteArtistSerializer, \
    ProfilePictureSerializer


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
        if self.action in ('create', 'list', 'retrieve'):
            return []
        return super().get_permissions()

    @action(methods=['patch'], detail=True, serializer_class=ProfilePictureSerializer)
    def update_profile_pricture(self, request, pk=None):
        user = self.get_object()
        try:
            profile_picture = user.profile_picture
            serializer = ProfilePictureSerializer(profile_picture, data={'picture': request.FILES['picture']},
                                                  partial=True)
        except: # TODO Search for good exception
            data = {'user': request.user.pk, 'picture': request.FILES['picture']}
            serializer = ProfilePictureSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['post'], detail=True, serializer_class=UserFollowingSerializer)
    def follow(self, request, pk=None):
        user = self.get_object()
        serializer = UserFollowingSerializer(data=request.data, context={'request': request, 'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        devices = user.gcmdevice_set
        for device in devices.filter(active=True):
            device.send_message(
                title=f'{request.user.username} vous suit',
                extra={
                    "route": f"/artist/{user.pk}"
                }
            )
        return Response(serializer.data)

    @action(methods=['delete'], detail=True, serializer_class=UserFollowingSerializer)
    def unfollow(self, request, pk=None):
        queryset = request.user.user_followed.filter(target=pk)
        if not queryset.exists():
            raise Http404
        queryset.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SoundViewSet(ProtectedManagementViewSet):
    queryset = Sound.objects.all()
    serializer_class = SoundSerializer

    def _verify_self(self, request):
        return request.user.sounds.filter(pk=self.kwargs['pk']).exists()

    def get_permissions(self):
        perms = super().get_permissions()
        if self.action in ('retrieve', 'list'):
            perms = []
        if self.action in ('update', 'partial_update', 'delete'):
            perms += [permissions.OR(IsSelf(self._verify_self), permissions.IsAdminUser())]
        return perms

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return CompleteSoundSerializer
        return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        self.get_object().file.delete()
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        result = super().create(request, *args, **kwargs)
        sound = self.get_object()
        poster = sound.added_by
        followers = poster.followers.all()
        for follower in followers:
            devices = follower.gcmdevice_set.filter(active=True)
            for device in devices:
                device.send_message(
                    f'{poster.username} a ajouté un nouveau son: {sound.title}',
                    title=f'{poster.username} a ajouté un nouveau son',
                    extra={
                        "route": f"/details/{sound.pk}"
                    }
                )
        return result

    @action(methods=['POST'], detail=True, serializer_class=SoundCommentSerializer)
    def comment(self, request, pk=None):
        sound = self.get_object()
        serializer = SoundCommentSerializer(data=request.data, context={'request': request, 'sound': sound})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer.search_tags_and_notify(serializer.data['message'])
        devices = sound.added_by.gcmdevice_set
        for device in devices.filter(active=True):
            device.send_message(
                f"{request.user.username} a commenté votre son {sound.title}.",
                title=f'{sound.title} nouveau commentaire',
                extra={
                    "route": f"/details/{sound.pk}#{serializer.data['id']}"
                }
            )
        return Response(serializer.data)

    @action(methods=['post'], detail=True, serializer_class=SoundLikeSerializer)
    def like(self, request, pk=None):
        sound = self.get_object()
        serializer = SoundLikeSerializer(data=request.data, context={'request': request, 'sound': sound})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        devices = sound.added_by.gcmdevice_set
        for device in devices.filter(active=True):
            device.send_message(f"{request.user.username} a aime votre son {sound.title}.")
        return Response(serializer.data)

    @action(methods=['delete'], detail=True, serializer_class=SoundLikeSerializer)
    def unlike(self, request, pk=None):
        queryset = request.user.sound_likes.filter(sound=pk)
        if not queryset.exists():
            raise Http404
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompleteAlbumSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return []
        return super().get_permissions()


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompleteArtistSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return []
        return super().get_permissions()


class PlaylistViewSet(ProtectedManagementViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def _verify_self(self, request):
        return request.user.playlists.filter(pk=self.kwargs['pk']).exists()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompletePlaylistSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return []
        return super().get_permissions()

    @action(methods=['POST'], detail=True, serializer_class=PlaylistCommentSerializer)
    def comment(self, request, pk=None):
        playlist = self.get_object()
        serializer = PlaylistCommentSerializer(data=request.data, context={'request': request, 'playlist': playlist})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        devices = playlist.added_by.gcmdevice_set
        for device in devices.filter(active=True):
            device.send_message(f"{request.user.username} a commenté votre playlist {playlist.title}.")
        return Response(serializer.data)

    @action(methods=['post'], detail=True, serializer_class=PlaylistLikeSerializer)
    def like(self, request, pk=None):
        playlist = self.get_object()
        serializer = PlaylistLikeSerializer(data=request.data, context={'request': request, 'playlist': playlist})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        devices = playlist.added_by.gcmdevice_set
        for device in devices.filter(active=True):
            device.send_message(f"{request.user.username} a aimé votre playlist {playlist.title}.")
        return Response(serializer.data)

    @action(methods=['delete'], detail=True, serializer_class=PlaylistLikeSerializer)
    def unlike(self, request, pk=None):
        queryset = request.user.playlist_likes.filter(playlist=pk)
        if not queryset.exists():
            raise Http404
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True, serializer_class=PlaylistFollowingSerializer)
    def follow(self, request, pk=None):
        playlist = self.get_object()
        serializer = PlaylistFollowingSerializer(data=request.data, context={'request': request, 'playlist': playlist})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['delete'], detail=True, serializer_class=PlaylistFollowingSerializer)
    def unfollow(self, request, pk=None):
        queryset = request.user.playlist_followed.filter(target=pk)
        if not queryset.exists():
            raise Http404
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetProfile(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = CompleteUserSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def retrieve(self, request, *args, **kwargs):
        self.kwargs['pk'] = request.user.pk
        return super().retrieve(request, *args, **kwargs)


class UpdateProfilePicture(generics.UpdateAPIView):
    serializer_class = ProfilePictureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def verify_self(self, request):
        try:
            profile_picture = request.user.profile_picture
            return int(profile_picture.user.pk) == int(request.user.pk)
        except:
            return True

    def get_queryset(self):
        return ProfilePicture.objects.filter(user=self.request.user.pk)

    def get_permissions(self):
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        self.kwargs['pk'] = request.user.profile_picture.pk
        if request.method == 'PATCH':
            return super().update(request, *args, **kwargs)
        raise NotImplementedError('Only partial update is allow')


class MusicStyleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MusicStyle.objects.all()
    serializer_class = MusicStyleSerializer
    permission_classes = []


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        models.ProfilePicture.objects.create(user=instance)
