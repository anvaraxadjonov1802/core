from itertools import product

from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    # path('products/<int:product_id>', views.product_detail, name='product_detail'),
    path('products/<int:product_id>', views.create_order, name='create_order'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('my-orders/', views.user_orders, name='user_orders'),
    path('admin_page/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_page/orders/', views.get_orders, name='get_orders'),
    path('admin_page/products/', views.get_products, name='get_products'),
    path('admin_page/users/', views.get_users_list, name='get_users_list'),
    path('admin_page/orders/<int:order_id>/', views.update_order, name='update_order'),
    path('admin_page/products/<int:product_id>/', views.update_product, name='update_product'),
    path('admin_page/product/delete/<int:product_id>', views.delete_product, name='delete_product' ),
]