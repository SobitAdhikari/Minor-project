from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

    def validate(self, data):
        if data['expense_type'] == 'fixed':
            if not data.get('recurrence_interval') or not data.get('next_due_date'):
                raise serializers.ValidationError("Recurring expenses must have recurrence_interval and next_due_date.")
        return data
