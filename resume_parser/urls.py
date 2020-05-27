from django.urls import path
from . import views


urlpatterns = [
    path("home", views.index, name="Index"),
    path("filtered", views.filter, name="Filter"),
    path("", views.index, name="Index")
]
