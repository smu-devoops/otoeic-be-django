from django.urls import path

from . import views

urlpatterns = [
    path('word', views.WordListRestAPI.as_view()),
    path('word/<int:id>', views.WordRestAPI.as_view()),
]
