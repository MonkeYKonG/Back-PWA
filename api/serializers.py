from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import User, Sound, Album, Playlist, Artist, SoundComment, UserFollowing, PlaylistFollowing, SoundLike, \
    PlaylistLike, MusicStyle, PlaylistComment, ProfilePicture


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePicture
        fields = ('picture', 'user')
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def update(self, instance, validated_data):
        if 'picture' in validated_data:
            instance.picture.delete()
        return super().update(instance, validated_data)


class MusicStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicStyle
        fields = ('id', 'name')


class BaseCommentSerializer(serializers.ModelSerializer):
    def search_tags_and_notify(self, message: str):
        tags = self.get_tags(message)
        for tag in tags:
            self.notify_tagged_user(tag)

    def notify_tagged_user(self, tag: str):
        queryset = User.objects.filter(username=tag)
        if queryset.exists():
            for user in queryset:
                self.send_notification_to_devices(user)

    def send_notification_to_devices(self, user: User):
        devices = user.gcmdevice_set.filter(active=True)
        sender = self.instance.post_by
        for device in devices:
            device.send_message(
                f'{self.instance.message}',
                extra={
                    'title': f'{sender.username} vous a tagué',
                    "route": f"/details/{self.instance.sound.pk}#{self.instance.pk}"
                }
            )

    def get_tags(self, message: str) -> list[str]:
        tags = []
        split_message = message.split(' ')
        for word in split_message:
            if len(word) > 1 and word.startswith('@'):
                tags.append(word[1:])
        return tags


class SoundCommentSerializer(BaseCommentSerializer):
    class Meta:
        model = SoundComment
        fields = ('id', 'sound', 'post_by', 'added_on', 'message')

    def create(self, validated_data):
        validated_data['post_by'] = self.context['request'].user
        validated_data['sound'] = self.context['sound']
        return super().create(validated_data)


class PlaylistCommentSerializer(BaseCommentSerializer):
    class Meta:
        model = PlaylistComment
        fields = ('id', 'playlist', 'post_by', 'added_on', 'message')

    def create(self, validated_data):
        validated_data['post_by'] = self.context['request'].user
        validated_data['playlist'] = self.context['playlist']
        return super().create(validated_data)


class SoundLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoundLike
        fields = ('id', 'sound', 'added_by')

    def validate(self, attrs):
        new_attrs = {'added_by': self.context['request'].user, 'sound': self.context['sound']}
        UniqueTogetherValidator(
            queryset=SoundLike.objects.all(),
            fields=['added_by', 'sound']
        )(new_attrs, self)
        return super().validate(new_attrs)

    def create(self, validated_data):
        validated_data['added_by'] = self.context['request'].user
        validated_data['sound'] = self.context['sound']
        return super().create(validated_data)


class PlaylistLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistLike
        fields = ('id', 'playlist', 'added_by')

    def validate(self, attrs):
        new_attrs = {'added_by': self.context['request'].user, 'playlist': self.context['playlist']}
        UniqueTogetherValidator(
            queryset=PlaylistLike.objects.all(),
            fields=['added_by', 'playlist']
        )(new_attrs, self)
        return super().validate(new_attrs)

    def create(self, validated_data):
        validated_data['added_by'] = self.context['request'].user
        validated_data['playlist'] = self.context['playlist']
        return super().create(validated_data)


class MinimalSoundSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True, source='likers.count')
    comment_count = serializers.IntegerField(read_only=True, source='comments.count')

    class Meta:
        model = Sound
        fields = (
            'id', 'title', 'style', 'file', 'added_on', 'like_count', 'comment_count')


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'title', 'picture', 'added_by')

    def update(self, instance, validated_data):
        if 'picture' in validated_data:
            instance.picture.delete()
        return super().update(instance, validated_data)

    def create(self, validated_data):
        print(self.context['request'])
        validated_data['added_by'] = self.context['request'].user
        return super().create(validated_data)


class CompleteAlbumSerializer(AlbumSerializer):
    sounds = MinimalSoundSerializer(many=True, read_only=True)

    class Meta(AlbumSerializer.Meta):
        fields = AlbumSerializer.Meta.fields + ('sounds',)


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name',)


class CompleteArtistSerializer(ArtistSerializer):
    sounds = MinimalSoundSerializer(many=True, read_only=True)

    class Meta(ArtistSerializer.Meta):
        fields = ArtistSerializer.Meta.fields + ('sounds',)


class SoundSerializer(MinimalSoundSerializer):
    class Meta(MinimalSoundSerializer.Meta):
        fields = MinimalSoundSerializer.Meta.fields + (
            'album', 'added_by',
        )

    def create(self, validated_data):
        validated_data['added_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'file' in validated_data:
            instance.file.delete()
        return super().update(instance, validated_data)


class CompleteSoundSerializer(SoundSerializer):
    comments = SoundCommentSerializer(many=True, read_only=True)
    album = AlbumSerializer(read_only=True)

    class Meta(SoundSerializer.Meta):
        fields = SoundSerializer.Meta.fields + ('comments',)


class MinimalPlaylistSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True, source='likers.count')
    sound_count = serializers.IntegerField(read_only=True, source='sounds.count')
    followers = serializers.IntegerField(read_only=True, source='followers.count')
    comment_count = serializers.IntegerField(read_only=True, source='comments.count')

    class Meta:
        model = Playlist
        fields = ('id', 'title', 'added_on', 'like_count', 'sound_count', 'followers', 'comment_count')

    def create(self, validated_data):
        validated_data['added_by'] = self.context['request'].user
        return super().create(validated_data)


class PlaylistSerializer(MinimalPlaylistSerializer):
    comments = PlaylistCommentSerializer(read_only=True, many=True)

    class Meta(MinimalPlaylistSerializer.Meta):
        fields = MinimalPlaylistSerializer.Meta.fields + ('sounds', 'added_by', 'comments')


class MinimalUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(read_only=True, source='profile_picture.picture')

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'profile_picture')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class CompletePlaylistSerializer(PlaylistSerializer):
    sounds = MinimalSoundSerializer(many=True, read_only=True)
    added_by = MinimalUserSerializer(read_only=True)
    comments = PlaylistCommentSerializer(many=True, read_only=True)

    class Meta(PlaylistSerializer.Meta):
        fields = PlaylistSerializer.Meta.fields + ('comments',)


class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ('id', 'added_by', 'target')

    def validate(self, attrs):
        new_attrs = {'added_by': self.context['request'].user, 'target': self.context['user']}
        UniqueTogetherValidator(
            queryset=UserFollowing.objects.all(),
            fields=['added_by', 'target']
        )(new_attrs, self)
        return super().validate(new_attrs)

    def create(self, validated_data):
        validated_data['added_by'] = self.context['request'].user
        validated_data['target'] = self.context['user']
        return super().create(validated_data)


class PlaylistFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistFollowing
        fields = ('id', 'added_by', 'target')

    def validate(self, attrs):
        new_attrs = {'added_by': self.context['request'].user, 'target': self.context['playlist']}
        UniqueTogetherValidator(
            queryset=PlaylistFollowing.objects.all(),
            fields=['added_by', 'target']
        )(new_attrs, self)
        return super().validate(new_attrs)

    def create(self, validated_data):
        validated_data['added_by'] = self.context['request'].user
        validated_data['target'] = self.context['playlist']
        return super().create(validated_data)


class UserSerializer(MinimalUserSerializer):
    sounds_count = serializers.IntegerField(read_only=True, source='sounds.count')
    playlists_count = serializers.IntegerField(read_only=True, source='playlists.count')
    sounds = MinimalSoundSerializer(read_only=True, many=True)
    playlists = MinimalPlaylistSerializer(read_only=True, many=True)
    followers = serializers.IntegerField(read_only=True, source='followers.count')
    followed = serializers.IntegerField(read_only=True, source='user_followed.count')
    albums = AlbumSerializer(read_only=True, many=True)

    class Meta(MinimalUserSerializer.Meta):
        fields = MinimalUserSerializer.Meta.fields + (
        'sounds_count', 'playlists_count', 'sounds', 'playlists', 'followers', 'followed', 'albums')


class CompleteUserSerializer(MinimalUserSerializer):
    notification_subscription = serializers.CharField(read_only=True, source='notification_subscription.token')
    sounds = MinimalSoundSerializer(read_only=True, many=True)
    playlists = MinimalPlaylistSerializer(read_only=True, many=True)
    albums = AlbumSerializer(read_only=True, many=True)
    sound_comments = SoundCommentSerializer(read_only=True, many=True)
    playlist_comments = PlaylistCommentSerializer(read_only=True, many=True)
    followers = UserFollowingSerializer(read_only=True, many=True)
    followed = serializers.IntegerField(read_only=True, source='user_followed.count')
    user_followed = UserFollowingSerializer(read_only=True, many=True)
    sound_likes = SoundLikeSerializer(read_only=True, many=True)
    playlist_likes = PlaylistLikeSerializer(read_only=True, many=True)

    class Meta(MinimalUserSerializer.Meta):
        fields = '__all__'
