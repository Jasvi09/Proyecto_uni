from django.urls import path
from .views import index, dashboard, services, add_orders, my_orders, log_in, sign_up, log_out, seleccionar_pedido, verify_account, verify_profile, cancel_orders

urlpatterns = [
    path('log_in', log_in, name='log_in_customer'),
    path('sign_up', sign_up, name='sign_up_customer'),
    path('log_out', log_out, name='log_out_customer'),
    path('dashboard/', dashboard, name='dashboard_customer'),
    path('services/', services, name='services_customer'),
    path('add_orders/<str:service_type>/<int:service_id>', add_orders, name='add_orders_customer'),
    path('seleccionar_pedido/<int:service_id>', seleccionar_pedido, name='seleccionar_pedido'),
    path('my_orders/', my_orders, name='my_orders_customer'),
    path('cancel_orders/<str:service_type>/<int:order_id>', cancel_orders, name='cancel_orders_customer'),
    path('verify_account/<auth_token>' , verify_account, name="verify_account_customer"),
    path('verify_profile/', verify_profile , name='verify_profile_customer'),
]