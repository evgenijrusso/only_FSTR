# Generated by Django 5.0.4 on 2024-04-16 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passage', '0009_alter_pereval_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='', max_length=200, unique=True, verbose_name='Email'),
            preserve_default=False,
        ),
    ]
