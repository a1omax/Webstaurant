# Generated by Django 4.0.4 on 2022-07-17 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_cart_owner_username_cart_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.TextField(help_text="Введіть ім'я", verbose_name="Ім'я"),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_price',
            field=models.FloatField(help_text='Введіть ціну замовлення', verbose_name='Ціна замовлення'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_text',
            field=models.TextField(help_text='Введіть текст замовлення', verbose_name='Текст замовлення'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.TextField(help_text='Введіть номер телефону', verbose_name='Номер телефону'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(help_text='Введіть місцезнахоження', max_length=100, null=True, verbose_name='Місцезнаходження'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.TextField(default='+380', help_text='Введіть номер телефону', max_length=20, verbose_name='Номер телефону'),
        ),
    ]