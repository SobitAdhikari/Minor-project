from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class DashboardSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dashboard_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Settings"
