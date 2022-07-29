from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from django.conf import settings

from tg_bot import bot


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    location = models.CharField(
        max_length=100,
        null=True,
        verbose_name="Адреса",

    )
    phone_number = models.TextField(
        max_length=20,
        blank=True,
        verbose_name="Номер телефону",

    )
    additional_info = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Додаткова інформація'
    )

    def __str__(self):
        return f"{str(self.user)} \n" \
               f"{self.phone_number} \n" \
               f"{self.location} \n" \
               f"{self.additional_info} \n"

    @property
    def cart(self) -> Cart:
        return Cart.objects.get(profile=self)

    @property
    def username(self) -> models.TextField:
        return self.user.username

    @property
    def name(self) -> models.TextField:
        return self.user.first_name


class Order(models.Model):
    username = models.TextField()
    name = models.TextField(
        verbose_name="Ім'я",
    )
    phone_number = models.TextField(
        verbose_name="Номер телефону"
    )

    id = models.AutoField(
        primary_key=True,
        auto_created=True,
    )

    created = models.DateTimeField(
        default=timezone.now,
    )
    order_text = models.TextField(
        verbose_name="Текст замовлення"
    )
    order_price = models.FloatField(
        verbose_name="Ціна замовлення"
    )
    location = models.CharField(
        max_length=100,
        null=True,
        verbose_name="Адреса",

    )

    additional_info = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Додаткова інформація'
    )

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"Ім\'я: {self.name}\n" \
               f"-----------------------------\n" \
               f"Телефон: {self.phone_number}\n" \
               f"-----------------------------\n" \
               f"Номер замовленя: #{self.id}\n" \
               f"-----------------------------\n" \
               f"\tЗамовлення: \n" \
               f"\n{self.order_text}\n\n" \
               f"-----------------------------\n" \
               f"Додаткова інформація: \n{self.additional_info}\n" \
               f"-----------------------------\n" \
               f"Замовленя створено: \n" \
               f"{self.created}\n" \
               f"-----------------------------\n" \
               f"До сплати: {self.order_price} грн"


class Cart(models.Model):

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def create_order(self) -> Order:
        """
        Creates Order from self Cart
        """

        items = self.items
        order_text = "\n".join(str(item) for item in items)

        profile = self.profile

        return Order(
            username=profile.username,
            name=profile.name,
            phone_number=profile.phone_number,
            order_text=order_text,
            order_price=self.count_price,
            location=profile.location,
            additional_info=profile.additional_info,
        )

    @classmethod
    def clear_cart(cls, cart) -> None:
        if isinstance(cart, Cart):
            for item in cart.items:
                item.delete()

    @property
    def items(self,  *args, **kwargs) -> models.QuerySet:
        items = self.cartitems_set.all()
        return items

    def add(self, product, amount=1):
        create_dict = {
            'cart': self,
            'product': product,
            'amount': 0
        }

        item, _ = CartItems.objects.get_or_create(
            cart=self, product=product,
            defaults=create_dict
        )

        item.amount += amount
        item.save()

    @property
    def count_price(self) -> float:
        sum_ = sum(item.price for item in self.items)
        return sum_

    def __str__(self):
        return f"Кошик користувача {self.profile.name}"


class CartItems(models.Model):
    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'catalog.Dish',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField()

    @property
    def price(self) -> float:
        return self.product.price * self.amount

    def __str__(self):
        return f'{self.product.name}: {self.amount} шт'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Profile)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(
            profile=instance
        )


@receiver(post_save, sender=Order)
def send_order_to_bot(sender, instance, created, **kwargs):
    if created:
        bot.send_order(settings.CHAT_ID, str(instance))

