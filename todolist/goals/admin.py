from django.contrib import admin
from goals.models import GoalCategory, Goal, Board, BoardParticipant


class BoardParticipantInline(admin.TabularInline):
    model = BoardParticipant
    extra = 1  # Number of empty forms to display for adding new members


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_deleted')
    inlines = [BoardParticipantInline]


@admin.register(BoardParticipant)
class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ('board', 'user', 'role')


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "status", "priority",
                    "due_date", "user", "created", "updated")
    search_fields = ("title", "user")


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
