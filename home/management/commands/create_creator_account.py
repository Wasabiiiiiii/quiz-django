from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Create quiz creator account'

    def add_arguments(self, parser):
        parser.add_argument('user', type=str,
                            help='Creator account username')

    def handle(self, *args, **kwargs):
        try:
            username = kwargs['user']
            password = User.objects.make_random_password()
            creator_setup = User.objects.create_user(
                username=username, email='', password=password)
            creator_account = User.objects.get(username=username)
            creator_group = Group.objects.get(name='creator')
            creator_group.user_set.add(creator_account)
            self.stdout.write("Account {},  created with password {} ".format(
                username, password))
        except IntegrityError as e:
            self.stdout.write(
                "Username {} already present ".format(username))
        except Exception as e:
            self.stdout.write(
                "I got a Generic error, craete_groups command already run? {} ".format(str(e)))
