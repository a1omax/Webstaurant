from django.shortcuts import render, redirect

from users.models import Profile, CartItems
from .models import DishType, Dish
from django.views import generic


class DishTypeListView(generic.ListView):
    model = DishType
    context_object_name = 'dish_types'
    template_name = 'catalog/dishtype.html'


class DishTypeDetailView(generic.DetailView):
    model = DishType
    template_name = 'catalog/dishes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            user = self.request.user
            profile = Profile.objects.get(user=user)
            context = super().get_context_data()

            context['profile'] = profile
        return context

    def post(self, request, *args, **kwargs):

        user = request.user
        if not user.is_authenticated:
            return redirect('/accounts/login')

        profile = Profile.objects.get(user=user)

        dish_id = self.request.POST['dish_id']
        dish = Dish.objects.get(id=dish_id)
        profile.cart.add(dish)

        return redirect('to_cart')


def home(request):
    return render(request, "")





