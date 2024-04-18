from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserSerializer, PerevalSerializer, \
    LevelSerializer, CoordSerializer, ImageSerializer
from .models import User, Pereval, Level, Coord, Image


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PerevalViewSet(viewsets.ModelViewSet):  # permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Pereval.objects.all().order_by('-add_time')
    serializer_class = PerevalSerializer
    filterset_fields = ('beauty_title', 'title', 'user', )


""" По заданию. Можно работать по умолчанию и без метода create """


def create(self, request, *args, **kwargs):
    serializer = PerevalSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'Success',
                'id': serializer.instance.pk,
            })

    if status.HTTP_400_BAD_REQUEST:
        return Response(
            {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid request',
                'id': None,
            })

    if status.HTTP_500_INTERNAL_SERVER_ERROR:
        return Response(
            {
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Error during operation',
                'id': None,
            })
    return super().create(request, *args, **kwargs)


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class CoordViewSet(viewsets.ModelViewSet):
    queryset = Coord.objects.all()
    serializer_class = CoordSerializer

    """ Тестовая проверка метода 'custom_post' url=/api/coords/custom_post/"""
    @action(detail=False, methods=['POST'])
    def custom_post(self, request):
        return Response({'message': 'Custom POST action executed successfully.'})


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filterset_fields = ('pereval',)
