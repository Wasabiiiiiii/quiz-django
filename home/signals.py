from invitations.signals import invite_accepted
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from invitations.utils import get_invitation_model
from django.core.mail import send_mail


@receiver(invite_accepted)
def handler_invite_accepted(sender, email, **kwargs):
    password = User.objects.make_random_password()
    user = User.objects.create_user(username=email,
                                    email=email,
                                    password=password)

    partecipant_group = Group.objects.get(name='partecipant')
    partecipant_group.user_set.add(user)
    send_mail(
        'Account Activation',
        'Account: username ' + email + ' password: ' + password,
        'admin@example.com',
        [email]
    )
