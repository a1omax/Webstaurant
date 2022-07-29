from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AnonymousUser

from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView

from users.forms import ProfileForm, UserForm
from users.models import Profile, Cart, CartItems


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)

            return redirect('home')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/signup.html', context)


def out_view(request):
    logout(request)
    return redirect('login')


def profile_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':

        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user.first_name = user_form.cleaned_data.get("first_name")
            user.save()

            profile.phone_number = profile_form.cleaned_data.get('phone_number')
            profile.location = profile_form.cleaned_data.get('location')
            profile.additional_info = profile_form.cleaned_data.get('additional_info')
            profile.save()
        return redirect('home')
    else:
        context = {
            'user_form': UserForm(initial={
                    'first_name': user.first_name
            }),
            'profile_form': ProfileForm(initial={
                'phone_number': profile.phone_number,
                'location': profile.location,
                'additional_info': profile.additional_info,
            })
        }
        return render(request, 'users/profile_detail.html', context)


class CartView(CreateView):

    template_name = 'users/cart.html'
    context_object_name = 'cart_items'
    success_url = 'to_cart'
    model = CartItems
    fields = '__all__'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user = self.request.user

        profile = Profile.objects.get(user=user)
        cart = profile.cart
        items = cart.items

        context['items'] = items
        context['total_price'] = cart.count_price
        context['profile'] = profile
        context['user_form'] = UserForm(initial={
                    'first_name': user.first_name
        })
        context['profile_form'] = ProfileForm(initial={
                'phone_number': profile.phone_number,
                'location': profile.location,
                'additional_info': profile.additional_info,
            })

        return context

    def post(self, request, *args, **kwargs):

        user = self.request.user

        profile = Profile.objects.get(user=user)

        if "menu" in request.POST:
            return redirect('home')

        if 'create_order' in request.POST:
            user_form = UserForm(request.POST)
            profile_form = ProfileForm(request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                user.first_name = user_form.cleaned_data.get("first_name")
                user.save()

                profile.phone_number = profile_form.cleaned_data.get('phone_number')
                profile.location = profile_form.cleaned_data.get('location')
                profile.additional_info = profile_form.cleaned_data.get('additional_info')
                profile.save()

                order = profile.cart.create_order()
                order.save()
                Cart.clear_cart(profile.cart)

            return redirect('to_cart')

        item_id = self.request.POST.get('item_id', None)
        item = CartItems.objects.get(id=item_id)

        if "delete_item" in request.POST:
            item.delete()

        elif "add_item" in request.POST:
            item.amount += 1
            item.save()

        elif "subtract_item" in request.POST:
            item.amount -= 1
            item.save()

        if item.amount == 0:
            item.delete()

        return redirect('to_cart')
