from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now


class Expense(models.Model):
    EXPENSE_TYPE_CHOICES = [
        ('daily', 'Daily Expense'),
        ('fixed', 'Fixed Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='expense_app_expenses')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_type = models.CharField(max_length=10, choices=EXPENSE_TYPE_CHOICES, default='daily')
    date = models.DateField(default=timezone.now)  # For daily expense or the last occurrence for fixed
    description = models.TextField(blank=True, null=True)

    # For fixed expenses 
    recurrence_interval = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
        ],
        blank=True,
        null=True,
        help_text="How often the fixed expense recursively"
    )
    next_due_date = models.DateField(blank=True, null=True, help_text="Next due date for the fixed expense")

    def __str__(self):
        return f"{self.title} - Rs.{self.amount} ({self.expense_type})"

def update_next_due_date(expense):
    if expense.recurrence_interval == 'daily':
        expense.next_due_date += timedelta(days=1)
    elif expense.recurrence_interval == 'weekly':
        expense.next_due_date += timedelta(weeks=1)
    elif expense.recurrence_interval == 'monthly':
        # Simplest: add 30 days (better to use dateutil.relativedelta for exact months)
        expense.next_due_date += timedelta(days=30)
    elif expense.recurrence_interval == 'yearly':
        expense.next_due_date += timedelta(days=365)
    expense.save()
