from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeAPI.as_view())
]
