from django.urls import path

from bot import views


urlpatterns = [
    path("verify", views.BotUserVerifyView.as_view()),
]
