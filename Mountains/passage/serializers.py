from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import Coord, Level, Pereval, Image, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fio', 'email', 'phone']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class CoordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coord
        fields = ['latitude', 'longitude', 'height']  # "__all__"


class ImageSerializer(serializers.ModelSerializer):
    img = serializers.CharField(max_length=500)

    class Meta:
        model = Image
        fields = ['pk', 'title', 'img', 'uploaded_at', 'pereval']


class PerevalSerializer(serializers.ModelSerializer):
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

    # def create(self, validated_data, **kwargs):
    #     user = validated_data.pop('user')
    #     coord = validated_data.pop('coord')
    #     level = validated_data.pop('level')
    #     images = validated_data.pop('images')
    #
    #     user, created = User.objects.get_or_create(**user)
    #
    #     coord = Coord.objects.create(**coord)
    #     level = Level.objects.create(**level)
    #     pereval = Pereval.objects.create(**validated_data, user=user, coord=coord, level=level)
    #
    #     for img in images:
    #         image = img.pop('image')
    #         title = img.pop('title')
    #         Image.objects.create(title=title, image=image, pereval=pereval)
    #     return pereval
    #
    # def validate(self, value):
    #
    #     user_data = value['user']
    #
    #     if self.instance:
    #         if (user_data['email'] != self.instance.user.email or
    #                 user_data['fio'] != self.instance.user.fio or
    #                 user_data['phone'] != self.instance.user.phone):
    #             raise serializers.ValidationError()
    #     return value