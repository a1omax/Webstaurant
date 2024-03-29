# Generated by Django 4.0.4 on 2022-07-14 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DishType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введіть тип страви', max_length=100, verbose_name='Тип страви')),
                ('show_priority', models.IntegerField(help_text='Введіть пріорітет видачі типу страви', null=True, unique=True, verbose_name='Пріорітет')),
            ],
            options={
                'verbose_name_plural': 'Типи страв',
                'ordering': ['show_priority'],
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введіть стан', max_length=50, verbose_name='Стан')),
            ],
            options={
                'verbose_name_plural': 'Стани страв',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введіть назву страви', max_length=100, verbose_name='Назва страви')),
                ('price', models.FloatField(help_text='Введіть ціну страви', verbose_name='Ціна страви')),
                ('amount', models.CharField(default='порція', help_text='Введіть кількість страви', max_length=30, verbose_name='Кількість страви')),
                ('description', models.TextField(blank=True, default='', help_text='Введіть опис страви', max_length=300, verbose_name='Опис страви')),
                ('dish_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.dishtype')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='catalog.status')),
            ],
            options={
                'verbose_name_plural': 'Страви',
                'ordering': ['dish_type', 'status', 'name'],
            },
        ),
    ]
