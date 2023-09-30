from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from core.serializers import UserCreateSerializer

User = get_user_model()


class CreateUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
