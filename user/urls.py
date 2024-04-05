from django.urls import path
from user.views import UserDetailAPI,RegisterUserAPIView, LoginUserAPIView, AuthenticateAPIView
urlpatterns = [
  # path("get-details/<str:pk>",UserDetailAPI.as_view()),
  path('register/',RegisterUserAPIView.as_view()),
  path('login/',LoginUserAPIView.as_view()),
  path('auth/',AuthenticateAPIView.as_view())

  # login -> token auth
  # token return


  # token will 
]