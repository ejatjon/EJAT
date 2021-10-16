from django.urls import path, include
from . import views

urlpatterns = [
    # path("",views.insertData,),
    path("",views.Index.as_view()),
    path('<user_name>/', views.Index.as_view(),name=""),
]
# name="index"