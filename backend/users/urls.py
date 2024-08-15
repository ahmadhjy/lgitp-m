from django.urls import path
from .views import (
        register_api,
        login_api,
        logout_api,
        logout_all_api,
        user_api,
        update_email_api,
        update_password_api,
        update_customer_preferences_api,
        update_customer_locations_api,
        update_supplier_location_api)


urlpatterns = [
    path('update-customer-preferences/',
         update_customer_preferences_api, name='update-customer-preferences'),
    path('update-customer-locations/',
         update_customer_locations_api, name='update-customer-locations'),
    path('update-supplier-location/',
         update_supplier_location_api,
         name='update_supplier_location'),
    path('register/', register_api, name='register'),
    path('login/', login_api, name='login'),
    path('logout/', logout_api, name='logout'),
    path('logoutall/', logout_all_api, name='logoutall'),
    path('user/', user_api, name='user'),
    path('update-email/', update_email_api, name='update_email'),
    path('update-password/', update_password_api, name='update_password'),
]
