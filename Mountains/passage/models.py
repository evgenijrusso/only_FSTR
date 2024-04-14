from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import CheckConstraint, Q


class User(models.Model):
    fio = models.CharField(max_length=250, verbose_name='Family mame')
    email = models.EmailField(max_length=200, blank=True, null=True, verbose_name='Email')
    phone = models.CharField(
        max_length=20, verbose_name='Phone',
        blank=True, null=True,
        validators=[RegexValidator(regex='^(\+?\d{1,3})?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$')],
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f'{self.fio} {self.email}'


class Pereval(models.Model):

    STATUS = (
        ("new", 'новый'),
        ("pending", 'В ожидании'),
        ("accepted", 'Принято'),
        ("rejected", 'Отклонено'),
    )

    beauty_title = models.CharField(max_length=200, verbose_name='Beauty title')
    title = models.CharField(max_length=200, verbose_name='Title')
    other_titles = models.TextField(blank=True, null=True, verbose_name='Other titles')
    connect = models.TextField(blank=True, null=True, verbose_name='Connect')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Add time')
    status = models.CharField(max_length=15, choices=STATUS, verbose_name='status', default='new')

    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='User')
    coord = models.OneToOneField('Coord', on_delete=models.CASCADE, verbose_name='Coord')
    level = models.ForeignKey('Level', on_delete=models.CASCADE, verbose_name='Level')

    class Meta:
        verbose_name = _("Pereval")
        verbose_name_plural = _("Perevals")

    def __str__(self):
        return f'{self.title} {self.status}'


class Level(models.Model):
    very_easy = 'A1'
    easy = 'A2'
    middle = 'B'
    rough = 'C1'
    very_rough = 'C2'

    CHOICE_LEVEL = (
        (very_easy, _('Very Easy')),
        (easy, _('Easy')),
        (middle, _('Middle')),
        (rough, _('Rough')),
        (very_rough, _('Very Rough')),
    )

    winter = models.CharField(max_length=2, choices=CHOICE_LEVEL, verbose_name="Winter level", default='Very easy')
    summer = models.CharField(max_length=2, choices=CHOICE_LEVEL, verbose_name="Spring level", default='Very easy')
    autumn = models.CharField(max_length=2, choices=CHOICE_LEVEL, verbose_name="Summer level", default='Very easy')
    spring = models.CharField(max_length=2, choices=CHOICE_LEVEL, verbose_name="Auturn level", default='Very easy')

    class Meta:
        verbose_name = _("Level")
        verbose_name_plural = _("Levels")

    def __str__(self):
        return f'Уровни сложности перевала: Winter: {self.winter}, Summer: {self.summer}, ' \
               f'Autumn: {self.autumn}, Spring: {self.spring}.'


class Coord(models.Model):
    latitude = models.FloatField(
        max_length=20,
        validators=[MinValueValidator(40), MaxValueValidator(80)],
        verbose_name='Latitude'
    )  # широта
    longitude = models.FloatField(
        max_length=20,
        validators=[MinValueValidator(0), MaxValueValidator(180)],
        verbose_name='Longitude'
    )  # долгота
    height = models.IntegerField(verbose_name='Height', default=0)

    class Meta:
        # constraints = CheckConstraint(
        #     check=Q(latitude__gte=-90) & Q(latitude__lte=90),
        #     name='coords_latitude__range'
        # )
        verbose_name = _('Coord')
        verbose_name_plural = _('Coords')

    def str(self):
        return f'Height: {self.height}, Latitude: {self.latitude}, Longitude: {self.longitude}.'


class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE,  null=True, blank=True,  related_name='images')

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return f'{self.title}'

