# from django.db import models
# from django.contrib.auth.models import User

# class Goal(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     target_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     saved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     deadline = models.DateField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def progress_percentage(self):
#         if self.target_amount == 0:
#             return 0
#         return min(100, (self.saved_amount / self.target_amount) * 100)

#     def __str__(self):
#         return f"{self.title} ({self.progress_percentage():.2f}%)"
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Goal(models.Model):
    DEFAULT_CHOICES = [
        ('Emergency Fund', 'Emergency Fund'),
        ('Vacation', 'Vacation'),
        ('New Car', 'New Car'),
        ('Education', 'Education'),
        ('Home Purchase', 'Home Purchase'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    default_title = models.CharField(max_length=100, choices=DEFAULT_CHOICES, blank=True)
    custom_title = models.CharField(max_length=100, blank=True)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    saved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField(default=timezone.now)

    def __str__(self):
        return self.custom_title or self.default_title

    @property
    def title(self):
        return self.custom_title or self.default_title

    @property
    def progress_percentage(self):
        if self.target_amount > 0:
            return (self.saved_amount / self.target_amount) * 100
        return 0
