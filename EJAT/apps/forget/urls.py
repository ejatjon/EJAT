from django.urls import path, include
from EJAT.apps.forget import views

urlpatterns = [
    path('', views.ForgotPassword.as_view(),name="forget"),
    path('emailverification/', views.emailverificationChecked),
    path('emailChecked/', views.emailChecked),
]
