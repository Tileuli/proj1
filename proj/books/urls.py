from django.urls import path
from .views import admin_page, create_item, delete_item, item_list, update_item, register, login_view, send_email, \
    product_detail, cart_add, cart_remove, cart_detail, order_create, order_detail, order_cancel, order_purchase, \
    order_payment, profile_view, search_results
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', item_list, name='item_list'),
    path('admin_page/', admin_page, name='admin_page'),
    path('create_item/', create_item, name='create_item'),
    path('delete_item/<int:id>/', delete_item, name='delete_item'),
    path('update_item/<int:id>/', update_item, name='update_item'),
    path('search/', search_results, name='search_results'),
    path('accounts/login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('register/', register, name='register'),
    path('send_email/', send_email, name='send_email'),
    path('product/<str:name>/', product_detail, name='product_detail'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<str:name>/', cart_add, name='cart_add'),
    path('cart/remove/<str:name>/', cart_remove, name='cart_remove'),
    path('order_create', order_create, name='order_create'),
    path('order_detail/<int:order_id>/', order_detail, name='order_detail'),
    path('order/<int:order_id>/cancel/', order_cancel, name='order_cancel'),
    path('order/purchase/<int:order_id>/', order_purchase, name='order_purchase'),
    path('order/payment/<int:order_id>/', order_payment, name='order_payment'),
]
