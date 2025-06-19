from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'title', 'amount', 'expense_type', 'date',
            'description', 'recurrence_interval', 'next_due_date'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'next_due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        expense_type = cleaned_data.get('expense_type')
        recurrence_interval = cleaned_data.get('recurrence_interval')
        next_due_date = cleaned_data.get('next_due_date')

        if expense_type == 'fixed':
            if not recurrence_interval or not next_due_date:
                raise forms.ValidationError("Recurring expenses must have a recurrence interval and next due date.")
        return cleaned_data
