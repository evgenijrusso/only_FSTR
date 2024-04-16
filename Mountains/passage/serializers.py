from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import Coord, Level, Pereval, Image, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'fio', 'email', 'phone']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class CoordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coord
        fields = ['latitude', 'longitude', 'height']  # "__all__"


class ImageSerializer(serializers.ModelSerializer):
    img = serializers.URLField()

    class Meta:
        model = Image
        fields = ['pk', 'title', 'img', 'uploaded_at', 'pereval']


class PerevalSerializer(WritableNestedModelSerializer):
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    status = serializers.CharField(read_only=True)
    user = UserSerializer()
    coord = CoordSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Pereval
        fields = [
            'pk', 'beauty_title', 'title', 'other_titles', 'connect',
            'add_time', 'status', 'user', 'coord', 'level', 'images'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'status': {'read_only': True},
        }