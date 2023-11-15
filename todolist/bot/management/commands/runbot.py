from django.core.management.base import BaseCommand, CommandError
from bot.management.commands.bot_manager import BotManager

from todolist.settings import TG_TOKEN


class Command(BaseCommand):
    help = "TG Bot to set and maintain goals"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('БОТ ЗАПУЩЕН!'))
        bot_manager = BotManager(TG_TOKEN)
        bot_manager.run_bot()

        self.stdout.write(self.style.SUCCESS('БОТ ВЫКЛЮЧЕН'))
