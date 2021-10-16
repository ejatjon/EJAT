import django.conf.locale


from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Contacts.as_view(),name=""),
]
