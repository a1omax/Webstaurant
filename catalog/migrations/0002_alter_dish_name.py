# Generated by Django 4.0.4 on 2022-07-16 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='name',
            field=models.CharField(help_text='Введіть назву страви', max_length=100, unique=True, verbose_name='Назва страви'),
        ),
    ]
