from django import forms
from .models import Income
from expenses.models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'expense_type', 'date', 'description', 'recurrence_interval', 'next_due_date']

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date']