from django.urls import path

from . import views

urlpatterns = [
    path('exam', views.UnsubmittedExamCreateView.as_view()),
    path('exam/<int:id>', views.UnsubmittedExamRetrieveView.as_view()),
    path('exam/<int:id>/submit', views.ExamSubmitRestAPI.as_view()),
]
