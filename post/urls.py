from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index, name="dashboard"),
    path('datail/<int:id>',views.postdetails,name="postDetails"),
    path('categoryList/<int:id>',views.CategoryPost,name="CategoryPost"),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('logout',views.logout,name='logout'),
    path('add-to-cart/<int:product_id>/', views.add_to_card, name='add_to_cart'),
    path('cart/',views.view_cart,name='cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase_quantity/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('datail/<int:post_id>/', views.add_comment, name='add_comment'),
    path('contact',views.Contact, name="contact"),
    path('feedback',views.Feedback,name="feedback"),
    path('checkout',views.checkout,name="checkout"),
    path('send_email/', views.send_email, name='send_email'),

]
