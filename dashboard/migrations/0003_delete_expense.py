# Generated by Django 4.2 on 2025-06-12 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_expense_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Expense',
        ),
    ]
