# //For html
from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense
from django.contrib.auth.decorators import login_required

@login_required
def expense_create_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard:dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/create_expense.html', {'form': form})

@login_required
def expense_list_view(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses/list_expenses.html', {'expenses': expenses})
# For DRF
from rest_framework import viewsets, permissions
from .models import Expense
from .serializers import ExpenseSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def delete_expense_view(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, f"Expense '{expense.title}' deleted.")
        return redirect('dashboard:dashboard')
    else:
        # Show a confirmation page or just redirect
        messages.warning(request, "Deletion must be via POST request.")
        return redirect('dashboard:dashboard')
  
 
     # or wherever you want to redirect
    # Optionally render a confirmation page if GET request

