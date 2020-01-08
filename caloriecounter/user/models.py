from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


# We use a custom user class to maintain the possibility to change the behaviour of the User model,
# because moving from the default's User model later on is a pain. For now, this class is still empty.
class User(AbstractUser):
    pass


# Generate a Token for each user new user created.
# See: https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
