from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Goal
from .forms import GoalForm, AddSavingsForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy


@login_required
def goal_list(request):
    goals = Goal.objects.filter(user=request.user)
    return render(request, 'goals/goal_list.html', {'goals': goals})


@login_required
def add_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            # ✅ Do NOT assign goal.title here
            goal.save()
            messages.success(request, "Goal created successfully!")
            return redirect('goals:goal_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = GoalForm()
    
    return render(request, 'goals/add_goal.html', {'form': form})


class GoalUpdateView(UpdateView):
    model = Goal
    form_class = GoalForm
    template_name = 'goals/goal_form.html'
    success_url = reverse_lazy('goals:goal_list')


class GoalDeleteView(DeleteView):
    model = Goal
    template_name = 'goals/goal_confirm_delete.html'
    success_url = reverse_lazy('goals:goal_list')


@login_required
def add_savings(request, pk):
    goal = get_object_or_404(Goal, pk=pk)

    if request.method == 'POST':
        form = AddSavingsForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            goal.saved_amount += amount
            goal.save()
            messages.success(request, 'Savings updated!')
            return redirect('goals:goal_list')
    else:
        form = AddSavingsForm()

    return render(request, 'goals/add_savings.html', {'form': form, 'goal': goal})
