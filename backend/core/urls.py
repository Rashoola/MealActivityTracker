# Here we have routes for API endpoints

from django.urls import path
from . import views

urlpatterns = [
    path("users/create/", views.create_user),
    path("users/login/", views.login),
    path("users/<int:user_id>/update/", views.update_user),
    path("users/<int:user_id>/generate-daily-plan/", views.generate_daily_plan),
    path("users/<int:user_id>/show-current-daily-plan/", views.show_current_daily_plan),
    path("foods/", views.fetch_all_foods),
    path("activities/", views.fetch_all_activities)
]