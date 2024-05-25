from django.urls import path

from . import views

urlpatterns = [
    path('exam', views.ExamListRestAPI.as_view()),
    path('exam/<int:id>', views.ExamRestAPI.as_view()),
    path('exam/<int:id>/submit', views.ExamSubmitRestAPI.as_view()),
]
