from rest_framework import permissions
from goals.models import Board, BoardParticipant


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class CategoryPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the request method is a safe method (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            # Users with any role can perform safe methods
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.board
            ).exists()

        # Check if the user is a board participant and has a role of owner or writer
        return BoardParticipant.objects.filter(
            user=request.user, board=obj.board, role__in=[
                BoardParticipant.Role.owner,
                BoardParticipant.Role.writer
            ]
        ).exists()


class CategoryCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        return BoardParticipant.objects.filter(
            user=request.user, board=Board.objects.get(pk=request.data.get('board')),
            role__in=[
                BoardParticipant.Role.owner,
                BoardParticipant.Role.writer
            ]
        ).exists()
