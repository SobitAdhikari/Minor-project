from django import forms
from .models import Goal
from django.core.exceptions import ValidationError

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['default_title', 'custom_title', 'target_amount', 'saved_amount', 'deadline']

        widgets = {
            'default_title': forms.Select(attrs={
                'id': 'id_default_title',
                'class': 'form-select',
            }),
            'custom_title': forms.TextInput(attrs={
                'id': 'id_custom_title',
                'placeholder': 'Or enter a custom goal title',
                'class': 'form-control',
            }),
            'target_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'saved_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        default_title = cleaned_data.get("default_title")
        custom_title = cleaned_data.get("custom_title")

        if not default_title and not custom_title:
            raise ValidationError("Please choose a default title or enter a custom title.")

        return cleaned_data


class AddSavingsForm(forms.Form):
    amount = forms.DecimalField(
        label="Add Amount",
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount to add',
        })
    )
