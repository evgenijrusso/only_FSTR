from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import UserSerializer, PerevalSerializer, \
    LevelSerializer, CoordSerializer, ImageSerializer
from .models import User, Pereval, Level, Coord, Image
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PerevalViewSet(viewsets.ModelViewSet):  # permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Pereval.objects.all().order_by('-add_time')
    serializer_class = PerevalSerializer
    filterset_fields = ('user', )

    def partial_update(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        save_pereval = get_object_or_404(Pereval.objects.all(), pk=pk)
        data = request.data.get('connect')
        serializer = PerevalSerializer(instance=save_pereval, data=request.data, partial=True)
        if serializer.is_valid():
            save_pereval = serializer.save()
            return Response({'connect': 'state = 1', 'message': 'Entry successfully modified'})
        return Response(code=400, data="wrong parameters")


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


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filterset_fields = ('pereval',)
