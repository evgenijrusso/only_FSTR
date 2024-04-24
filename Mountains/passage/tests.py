from passage.models import Coord, User, Level, Image, Pereval
from rest_framework.test import APITestCase
from rest_framework import status
from .serializers import PerevalSerializer


class MyTestCase(APITestCase):
    def setUp(self):
        # Перевал
        self.pass_1 = Pereval.objects.create(
            user=User.objects.create(
                fio='Иванов Петр Васильевич',
                email='Ivanov@mail.ru',
                phone='89999999999'
            ),
            beauty_title='beauty_title',
            title='title',
            other_titles='other_title',
            connect='connect',
            coord=Coord.objects.create(
                latitude=22.2,
                longitude=11.1,
                height=1000
            ),
            level=Level.objects.create(
                winter='1A',
                summer='1A',
                autumn='1A',
                spring='1A'
            ),
        )
        # Изображение для объекта перевал 1
        self.image_1 = Image.objects.create(
            title='Гора Вудъяврчорр',
            img='https://risk.ru/u/img/174/173816.jpg',
            pereval=self.pass_1
        )

    def test_pereval_list(self):
        """Тест endpoint /Pereval/ - список всех объектов модели PerevalAdded"""
        response = self.client.get('/submitData/')
        serializer_data = PerevalSerializer([self.pass_1], many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_pereval_detail(self):
        """Тест endpoint /Pereval/ - объект модели Pass по его id"""

        response = self.client.get(f'/submitData/{self.pass_1.id}/')
        serializer_data = PerevalSerializer(self.pass_1).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_pereval_user_email(self):
        """Тест endpoint /submitData/user__email=<email> - объекты модели Pass отфильтрованные по email пользователя"""

        email = self.pass_1.user.email
        url = f'/submitData/?user__email={email}'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# python manage.py test
