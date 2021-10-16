from django.urls import path, re_path
from . import views
urlpatterns=[
    path('<article_id>/',views.Single.as_view())
]