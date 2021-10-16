from django.urls import path, re_path
from . import views
urlpatterns=[
    path("",views.search),
    path('<filter>/',views.Search.as_view())
]