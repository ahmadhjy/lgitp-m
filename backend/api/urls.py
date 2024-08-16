from django.urls import path, include
from categories.views import get_categories
from rest_framework.routers import DefaultRouter  # <-- Add this line
from booking.views import (
    activity_booking_create,
    tour_booking_create,
    package_booking_create,
)
from dashboard.views import (
    supplier_dashboard,
    supplier_activity_bookings,
    customer_activity_bookings,
    confirm_activity_booking,
    confirm_payment,
    customer_package_bookings,
    customer_tour_bookings,
    supplier_packages_bookings,
    supplier_tours_bookings,
    confirm_package_booking,
    confirm_tour_booking,
    confirm_package_payment,
    confirm_tour_payment,
)
from activities.views import (
    get_activities,
    get_periods_by_offer_and_day,
    get_offers_by_activity,
    get_activity,
    get_all_activities,
)
from packages.views import get_packages, get_package_days, get_package, get_all_packages
from tours.views import get_tours, get_tour_days, get_tour, get_all_tours
from location.views import get_locations
from notifications.views import notification_list, mark_notification_as_read
from .views import latest_items_api, featured_items_api, search, for_you_items
from favorites.views import (
    favorite_activity,
    favorite_tour,
    favorite_package,
    all_favorites,
)
from blog.views import PostViewSet, upload_image


router = DefaultRouter()
router.register(r"posts", PostViewSet)

urlpatterns = [
    path("for-you/", for_you_items, name="for_you"),
    path("supplier-dashboard/", supplier_dashboard, name="supplier_dashboard"),
    path("all-favorites/", all_favorites, name="all_favorites"),
    path(
        "favorite-activity/<int:activity_id>/",
        favorite_activity,
        name="favorite_activity",
    ),
    path("favorite-tour/<int:tour_id>/", favorite_tour, name="favorite_tour"),
    path(
        "favorite-package/<int:package_id>/", favorite_package, name="favorite_package"
    ),
    path("search", search, name="search"),
    path("featured-items/", featured_items_api, name="featured-items"),
    path("latest/", latest_items_api, name="latest_items_api"),
    path("notifications/", notification_list, name="list_notification"),
    path(
        "readnotification/<int:pk>/",
        mark_notification_as_read,
        name="read_notification",
    ),
    path("categories/", get_categories, name="get_categories"),
    path("locations/", get_locations, name="get_locations"),
    path("activities/", get_activities, name="get_activities"),
    path("all-tours/", get_all_tours, name="get_all_tours"),
    path("all-packages/", get_all_packages, name="get_all_packages"),
    path("all-activities/", get_all_activities, name="get_all_activities"),
    path("activity/<int:pk>/", get_activity, name="get_activity"),
    path("packages/", get_packages, name="get_packages"),
    path("package/<int:pk>/", get_package, name="get_package"),
    path("tours/", get_tours, name="get_tours"),
    path("tour/<int:pk>/", get_tour, name="get_tour"),
    path(
        "packagedays/<int:package_offer_id>/", get_package_days, name="get_package_days"
    ),
    path("tourdays/<int:tour_offer_id>/", get_tour_days, name="get_tour_days"),
    path(
        "activity/<int:activity_id>/offers/",
        get_offers_by_activity,
        name="get_offers_by_activity",
    ),
    path(
        "offer/<int:offer_id>/periods/<str:day>/",
        get_periods_by_offer_and_day,
        name="get_daily_periods",
    ),
    path("bookingactivity/", activity_booking_create, name="create_activity_booking"),
    path(
        "supplier/bookings/",
        supplier_activity_bookings,
        name="supplier_activity_bookings",
    ),
    path(
        "customer/bookings/",
        customer_activity_bookings,
        name="customer_activity_bookings",
    ),
    path(
        "supplier/bookings/<int:booking_id>/confirm/",
        confirm_activity_booking,
        name="confirm_activity_booking",
    ),
    path(
        "supplier/bookings/<int:booking_id>/confirm-payment/",
        confirm_payment,
        name="confirm_activity_payment",
    ),
    path("bookingtour/", tour_booking_create, name="create_tour_booking"),
    path("bookingpackage/", package_booking_create, name="create_package_booking"),
    path(
        "supplier/packagesb/",
        supplier_packages_bookings,
        name="supplier_packages_bookings",
    ),
    path("supplier/toursb/", supplier_tours_bookings, name="supplier_tours_bookings"),
    path(
        "customer/toursb/",
        customer_tour_bookings,
        name="customer_tours_booking",
    ),
    path(
        "customer/packagesb/",
        customer_package_bookings,
        name="customer_package_bookings",
    ),
    path(
        "supplier/package/<int:booking_id>/confirm/",
        confirm_package_booking,
        name="confirm_package_booking",
    ),
    path(
        "supplier/tour/<int:booking_id>/confirm/",
        confirm_tour_booking,
        name="confirm_tour_booking",
    ),
    path(
        "supplier/package/<int:booking_id>/confirm-payment/",
        confirm_package_payment,
        name="confirm_package_payment",
    ),
    path(
        "supplier/tour/<int:booking_id>/confirm-payment/",
        confirm_tour_payment,
        name="confirm_tour_payment",
    ),
    path("upload-image/", upload_image, name="upload_image"),
    path("", include(router.urls)),  # This will handle /posts/ and /posts/<int:pk>/
]
