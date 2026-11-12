from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CampusProfile

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def ensure_campus_profile(sender,instance,created,**kwargs):
    if created:
        CampusProfile.objects.get_or_create(user=instance)
