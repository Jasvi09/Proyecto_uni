from django.urls import path
from .views import log_in, sign_up, log_out, dashboard, my_services, update_my_services, add_my_services, delete_my_services, orders, accept_orders, cancel_orders, verify_account, verify_profile, completed_orders

urlpatterns = [
    path('log_in', log_in, name='log_in_business'),
    path('sign_up', sign_up, name='sign_up_business'),
    path('log_out', log_out, name='log_out_business'),
    path('dashboard/', dashboard, name='dashboard_business'),
    path('my_services/', my_services, name='my_services_business'),
    path('add_my_services/', add_my_services, name='add_my_services_business'),
    path('update_my_services/<int:service_id>/', update_my_services, name='update_my_services_business'),
    path('delete_my_services/<int:service_id>/', delete_my_services, name='delete_my_services_business'),
    path('orders/', orders, name='orders_business'),
    path('completed_orders/<str:service_type>/<int:order_id>', completed_orders, name='completed_orders_business'),
    path('accept_orders/<str:service_type>/<int:order_id>', accept_orders, name='accept_orders_business'),
    path('cancel_orders/<str:service_type>/<int:order_id>', cancel_orders, name='cancel_orders_business'),
    path('verify_account/<auth_token>' , verify_account, name="verify_account_business"),
    path('verify_profile/', verify_profile , name='verify_profile_business'),
    # path('data_client/<int:order_id>', data_client , name='data_client_business'),
]