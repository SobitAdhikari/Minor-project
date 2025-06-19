from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# class Expense(models.Model):
#     EXPENSE_TYPE_CHOICES = [
#         ('daily', 'Daily Expense'),
#         ('fixed', 'Fixed Expense'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='dashboard_expenses')
#     title = models.CharField(max_length=200)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     expense_type = models.CharField(max_length=10, choices=EXPENSE_TYPE_CHOICES, default='daily')
#     date = models.DateField(default=timezone.now)
#     description = models.TextField(blank=True, null=True)

#     recurrence_interval = models.CharField(
#         max_length=20,
#         choices=[
#             ('daily', 'Daily'),
#             ('weekly', 'Weekly'),
#             ('monthly', 'Monthly'),
#             ('yearly', 'Yearly'),
#         ],
#         blank=True,
#         null=True
#     )
#     next_due_date = models.DateField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.title} - {self.amount} ({self.expense_type})"

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Income: {self.amount} on {self.date}"