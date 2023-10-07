from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    password_repeat = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password', 'password_repeat']
        # extra_kwargs = {'password_repeat': {'write_only': True}}

    def is_valid(self, *, raise_exception=False):
        password_repetion = self.initial_data.get('password_repeat', None)
        password = self.initial_data.get('password', None)
        if password and password != password_repetion:
            raise ValidationError('Пароли не совпадают!')
        validate_password(password)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_repeat')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # fields = ['username', 'password']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'),
                            username=username, password=password)
        if not user:
            raise serializers.ValidationError(
                'Incorrect Username or Password!')
        attrs['user'] = user
        return attrs


class UserRetrUpdSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
