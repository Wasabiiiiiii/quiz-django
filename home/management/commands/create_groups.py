from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Create partecipant and creator groups'

    def handle(self, *args, **kwargs):
        partecipant = Group.objects.get_or_create(name="partecipant")
        creator = Group.objects.get_or_create(name="creator")
        self.stdout.write("Groups created")
