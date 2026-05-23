# Here we have routes for API endpoints

from django.urls import path
from . import views

urlpatterns = [
    path("users/create/", views.create_user),
    path("users/login/", views.login)
]