from django.urls import path

from . import views

urlpatterns = [
    path('exam', views.ExamListCreateView.as_view()),
    path('exam/<int:id>', views.UnsubmittedExamRetrieveView.as_view()),
    path('exam/<int:id>/result', views.ExamResultRetrieveView.as_view()),
]
