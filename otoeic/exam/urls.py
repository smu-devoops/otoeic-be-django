from django.urls import path

from . import views

urlpatterns = [
    path('exam', views.UnsubmittedExamListCreateView.as_view()),
    path('exam/<int:id>', views.UnsubmittedExamRetrieveView.as_view()),
    path('exam/<int:id>/submit', views.ExamSubmitRestAPI.as_view()),
]
