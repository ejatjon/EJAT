
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Register.as_view(),name="register"),
    path('emailverification/',views.emailverificationChecked),
    path('emailChecked/',views.emailChecked),
    path('usernameChecked/',views.usernameChecked),
]
