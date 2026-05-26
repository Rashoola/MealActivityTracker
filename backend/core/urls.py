# Here we have routes for API endpoints

from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_user),
    path("login/", views.login),
    path("update/<int:user_id>/", views.update_user),
]