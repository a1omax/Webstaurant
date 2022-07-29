from django.db import models


class Status(models.Model):
    name = models.CharField(
        max_length=50,
        help_text="Введіть стан",
        verbose_name="Стан",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Стани страв"

    def __str__(self):
        return self.name


class DishType(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Введіть тип страви",
        verbose_name="Тип страви",
    )
    show_priority = models.IntegerField(
        unique=True,
        null=True,
        help_text="Введіть пріорітет видачі типу страви",
        verbose_name="Пріорітет",
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='images/dishtype'
    )

    class Meta:
        ordering = ["show_priority"]
        verbose_name_plural = "Типи страв"

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(
        unique=True,
        max_length=100,
        help_text="Введіть назву страви",
        verbose_name="Назва страви"
    )
    price = models.FloatField(
        help_text="Введіть ціну страви",
        verbose_name="Ціна страви",
    )
    amount = models.CharField(
        max_length=30,
        help_text="Введіть кількість страви",
        verbose_name="Кількість страви",
        default="порція"
    )
    description = models.TextField(
        max_length=300,
        help_text="Введіть опис страви",
        verbose_name="Опис страви",
        blank=True,
        default=''

    )
    dish_type = models.ForeignKey(
        'DishType',
        on_delete=models.PROTECT,
    )

    status = models.ForeignKey(
        'Status',
        on_delete=models.PROTECT,
        null=True,
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='images/dish'
    )

    class Meta:
        ordering = ["dish_type", "status", "name"]
        verbose_name_plural = "Страви"

    def __str__(self):
        return f"{self.name} {self.status}"

