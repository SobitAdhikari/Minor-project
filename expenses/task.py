from django.utils.timezone import now
from django.core.mail import send_mail
from .models import Expense

def notify_due_fixed_expenses():
    today = now().date()
    expenses_due = Expense.objects.filter(
        expense_type='fixed',
        next_due_date__lte=today,
        notified=False
    )

    for expense in expenses_due:
        # Send email notification (customize as needed)
        subject = f'Recurring Expense Due: {expense.title}'
        message = f'Your fixed expense "{expense.title}" of amount {expense.amount} is due on {expense.next_due_date}.'
        recipient_list = [expense.user.email]

        send_mail(subject, message, 'your_email@example.com', recipient_list)

        # Mark as notified to avoid duplicate notifications
        expense.notified = True
        expense.save()
