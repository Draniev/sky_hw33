from core.serializers import (UserCreateSerializer, UserLoginSerializer,
                              UserRetrUpdSerializer)
from django.contrib.auth import get_user_model, login, logout
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


class CreateUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class LoginUser(APIView):
    def post(self, request):

        serializer = UserLoginSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            login(request, user)

            return Response({'username': user.username, 'password': user.password},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileUser(RetrieveUpdateDestroyAPIView):
    # queryset = User.objects.all()
    serializer_class = UserRetrUpdSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the currently authenticated user
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
