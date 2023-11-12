from django.contrib.auth import get_user_model
from django.db.models.query import transaction
from rest_framework import serializers
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
# from core.models import User
from core.serializers import UserRetrUpdSerializer

User = get_user_model()


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    # def validate_board(self, value):
    #     # Check if the board with the provided ID exists and is valid
    #     try:
    #         board = Board.objects.get(pk=value.id)
    #     except Board.DoesNotExist:
    #         raise serializers.ValidationError("Board does not exist.")
    #     # You can add more custom validation here if needed.
    #     return value


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserRetrUpdSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "board")


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if not BoardParticipant.objects.filter(
                user=self.context["request"].user, board=value.board,
                role__in=[
                    BoardParticipant.Role.owner,
                    BoardParticipant.Role.writer,
                ]
                ).exists():
            raise serializers.ValidationError("not owner or writer of category")

        return value


class GoalSerializer(serializers.ModelSerializer):
    user = UserRetrUpdSerializer(read_only=True)
    category = GoalCreateSerializer

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if not BoardParticipant.objects.filter(
                user=self.context["request"].user, board=value.board,
                role__in=[
                    BoardParticipant.Role.owner,
                    BoardParticipant.Role.writer,
                ]
                ).exists():
            raise serializers.ValidationError("not owner or writer of category")

        return value


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_goal(self, value):
        if value.status == Goal.Status.archived:
            raise serializers.ValidationError("not allowed in deleted goal")

        if not BoardParticipant.objects.filter(
                user=self.context["request"].user, board=value.category.board,
                role__in=[
                    BoardParticipant.Role.owner,
                    BoardParticipant.Role.writer,
                ]
                ).exists():
            raise serializers.ValidationError("not owner or writer on this goal")

        return value


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserRetrUpdSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.Role
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance, validated_data):
        owner = validated_data.pop("user") # TODO: Либо править пользователей может только хозяин либо тут ошибка!
        new_participants = validated_data.pop("participants")
        new_by_id = {part["user"].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if (
                        old_participant.role
                        != new_by_id[old_participant.user_id]["role"]
                    ):
                        old_participant.role = new_by_id[old_participant.user_id][
                            "role"
                        ]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_part["user"], role=new_part["role"]
                )

            instance.title = validated_data["title"]
            instance.save()

        return instance
