from django.urls import path, include, re_path
from EJAT.apps.reset import views


urlpatterns = [
    path('<email>/',views.Reset.as_view())
]