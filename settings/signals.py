from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import DashboardSettings

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        DashboardSettings.objects.create(user=instance)
