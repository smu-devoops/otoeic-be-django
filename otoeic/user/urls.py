from django.urls import path

from . import views

urlpatterns = [
    path('user', views.UserRestAPI.as_view()),
]
