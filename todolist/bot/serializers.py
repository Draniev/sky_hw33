from rest_framework import serializers
from django.contrib.auth import get_user_model
from bot.models import TgUser

User = get_user_model()


class TgUserUpdSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TgUser
        read_only_fields = ("id", "state", "user")
        fields = "__all__"

    def validate_verification_code(self, value):
        try:
            tg_user = TgUser.objects.get(verification_code=value)

        except TgUser.DoesNotExist:
            raise serializers.ValidationError("Verification code is wrong!")

        return value

    def update(self, instance, validated_data):
        instance.user = self.context['request'].user
        instance.state = TgUser.State.confirmed
        instance.save()

        return instance
