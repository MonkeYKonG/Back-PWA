from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from api import models


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        models.ProfilePicture.objects.create(user=sender.pk)