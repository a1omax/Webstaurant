from django.test import TestCase
from users.models import Cart, User, CartItems, Profile, Order
from catalog.models import Dish, DishType, Status


class UsersTestCase(TestCase):
    def setUp(self):
        dish_type = DishType(name="aa", show_priority=12)
        dish_type.save()

        status = Status(name='True')
        status.save()

        dish = Dish(
            name="Канапка з ікрою",
            price=10.10,
            dish_type=dish_type,
            status=status
        )
        dish.save()

        user = User.objects.create_user('test2', 'test2')
        user.save()

        profile = user.profile

        cart = profile.cart


        cart_item1 = CartItems(cart=cart, product=dish, amount=1)
        cart_item1.save()

        cart_item2 = CartItems(cart=cart, product=dish, amount=1)
        cart_item2.save()

        self.cart = cart

    def test_create_order(self):
        order = Cart.create_order(self.cart)
        order.save()

        print(order)


