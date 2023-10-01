from django.urls import path, include
from core.views import CreateUser

urlpatterns = [
    path('signup', CreateUser.as_view()),
]
