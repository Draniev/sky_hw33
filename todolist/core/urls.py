from django.urls import path, include
from core.views import CreateUser, LoginUser, ProfileUser

urlpatterns = [
    path('signup', CreateUser.as_view()),
    path('login', LoginUser.as_view()),
    path('profile', ProfileUser.as_view()),
]
