# Generated by Django 5.0.4 on 2024-04-14 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passage', '0004_coord_remove_pereval_coords_pereval_coord_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pereval',
            options={'verbose_name': 'Pereval', 'verbose_name_plural': 'Perevals'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]