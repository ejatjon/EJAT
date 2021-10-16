from django.urls import path, re_path
from . import views
urlpatterns=[
    path('images/',views.upload_image)
]