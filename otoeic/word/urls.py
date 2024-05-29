from django.urls import path

from . import views

urlpatterns = [
    path('word', views.WordListCreateView.as_view()),
    path('word/<int:id>', views.WordManipulateView.as_view()),
]
