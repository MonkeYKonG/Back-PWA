from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework import serializers

from api.models import User, Sound, Album, Playlist, Artist, SoundComment, UserFollowing, PlaylistFollowing, SoundLike, \
    PlaylistLike, MusicStyle, PlaylistComment


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SlugRelatedField(read_only=True, slug_field='picture')
    sounds = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    playlists = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'email', 'first_name', 'last_name', 'profile_picture', 'sounds', 'playlists'
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class CompleteUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SlugRelatedField(read_only=True, slug_field='picture')
    notification_subscription = serializers.SlugRelatedField(read_only=True, slug_field='token')
    albums = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    sounds = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    playlists = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    sound_comments = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    playlist_comments = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    followers = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    sound_likes = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    playlist_likes = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class MusicStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicStyle
        fields = ('id', 'name')


class SoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sound
        fields = ('id', 'title', 'style', 'file', 'added_on', 'album', 'artist', 'added_by')

    def create(self, validated_data):
        validated_data['added_by'] = self.context['request'].user
        return super().create(validated_data)


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'title', 'picture')


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name',)


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('id', 'title', 'added_on', 'sounds', 'added_by')

    def create(self, validated_data):
        validated_data['added_by'] = self.context['request'].user
        return super().create(validated_data)


class SoundCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoundComment
        fields = ('id', 'sound', 'post_by', 'added_on', 'message')

    def create(self, validated_data):
        validated_data['post_by'] = self.context['request'].user
        return super().create(validated_data)


class PlaylistCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistComment
        fields = ('id', 'playlist', 'post_by', 'added_on', 'message')

    def create(self, validated_data):
        validated_data['post_by'] = self.context['request'].user
        return super().create(validated_data)


class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ('id', 'added_by', 'target')

    def create(self, validated_data):
        validated_data['added_by'] = self.context['request'].user
        return super().create(validated_data)


class PlaylistFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistFollowing
        fields = ('id', 'added_by', 'target')

    def create(self, validated_data):
        validated_data['added_by'] = self.context['request'].user
        return super().create(validated_data)


class SoundLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoundLike
        fields = ('id', 'sound', 'added_by')

    def create(self, validated_data):
        validated_data['added_by'] = self.context['request'].user
        return super().create(validated_data)


class PlaylistLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistLike
        fields = ('id', 'playlist', 'added_by')

    def create(self, validated_data):
        validated_data['added_by'] = self.context['request'].user
        return super().create(validated_data)
