from django.urls import path, include
from permission.views import *

urlpatterns = [
    path("home/", HomeView.as_view(), name="home_view"),
    path("home/<int:pk>/", HomeView.as_view(), name="home_update_view"),
]