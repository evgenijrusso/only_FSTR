from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin
from .models import Coord, Level, Pereval, Image, User


class UserSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'fio', 'email', 'phone']

        extra_kwargs = {
            'pk': {'read_only': True},
        }


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['pk', 'summer', 'autumn', 'winter', 'spring']


class CoordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coord
        fields = ['pk', 'latitude', 'longitude', 'height']  # "__all__"


class ImageSerializer(serializers.ModelSerializer):
    img = serializers.URLField()

    class Meta:
        model = Image
        fields = ['pk', 'title', 'img']


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
            'add_time', 'user', 'coord', 'level', 'images', 'status',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'status': {'read_only': True},
        }

    def create(self, validated_data, **kwargs):
        user = validated_data.pop('user')
        coord = validated_data.pop('coord')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        user, created = User.objects.get_or_create(**user)
        coord = Coord.objects.create(**coord)
        level = Level.objects.create(**level)
        pereval = Pereval.objects.create(**validated_data, user=user, coord=coord, level=level, status='new')

        for im in images:
            title = im.pop('title')
            img = im.pop('img')
            Image.objects.create(img=img, pereval=pereval, title=title)

        return pereval

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            validating_user_fields = [
                instance_user.fio != data_user['fio'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['email'],
            ]
            if data_user is not None and any(validating_user_fields):
                raise serializers.ValidationError({'Rejected': 'User data cannot be changed'})
        return data
