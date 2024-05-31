from django.urls import path

from . import views

urlpatterns = [
    path('user', views.UserListView.as_view()),
    path('user/<int:id>', views.UserManageView.as_view()),
    path('user/me', views.UserSelfManageView.as_view()),
    path('user/<int:id>/calendar', views.UserCalendarView.as_view()),
    path('user/me/calendar', views.UserSelfCalendarView.as_view()),
    path('user/register', views.UserRegisterView.as_view()),
    path('user/login', views.UserLoginView.as_view()),
    path('user/logout', views.UserLogoutView.as_view()),
    path('user/buy/freeze', views.UserBuyFreezeView.as_view()),
]
