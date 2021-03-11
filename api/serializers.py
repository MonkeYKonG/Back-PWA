from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework import serializers

from api.models import User, Sound, Album, Playlist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', "first_name", "last_name")
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class SoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sound
        fields = ("id", "title", 'style', 'file', 'added_on', 'album', 'added_by')

    def create(self, validated_data):
        validated_data['added_by'] = self.context['request'].user
        return super().create(validated_data)


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'title', 'added_on', 'date')

    def create(self, validated_data):
        validated_data['added_by'] = self.context['request'].user


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('id', 'title', 'added_on', 'sounds', 'added_by')

    def create(self, validated_data):
        validated_data['added_by'] = self.context['request'].user
