from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Public.as_view(),name=""),
]
