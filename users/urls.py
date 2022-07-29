from django.urls import path, include, re_path

from users import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_view, name='to_profile'),
    path('profile/cart', views.CartView.as_view(), name='to_cart'),
    path('profile/logout/', views.out_view, name='log_out')
]
