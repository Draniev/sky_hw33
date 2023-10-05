from django.urls import path, include
from core.views import CreateUser, LoginUser

urlpatterns = [
    path('signup', CreateUser.as_view()),
    path('login', LoginUser.as_view()),
]
