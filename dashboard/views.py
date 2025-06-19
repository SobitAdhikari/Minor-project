from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncMonth
from django.template.loader import render_to_string
from django.http import HttpResponse
from datetime import datetime
from django.utils.timezone import now
from .forms import ExpenseForm, IncomeForm
from expenses.models import Expense
from .models import Income

import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from xhtml2pdf import pisa


@login_required
def dashboard_view(request):
    income_form = IncomeForm()

    if request.method == 'POST' and 'amount' in request.POST:
        income_form = IncomeForm(request.POST)
        if income_form.is_valid():
            income = income_form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('dashboard:dashboard')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    expenses_qs = Expense.objects.filter(user=request.user)
    incomes_qs = Income.objects.filter(user=request.user)

    if start_date and end_date:
        expenses_qs = expenses_qs.filter(date__range=[start_date, end_date])
        incomes_qs = incomes_qs.filter(date__range=[start_date, end_date])

    income_total = incomes_qs.aggregate(Sum('amount'))['amount__sum'] or 0
    expense_total = expenses_qs.aggregate(Sum('amount'))['amount__sum'] or 0
    remaining = income_total - expense_total

    category_totals = expenses_qs.values('title').annotate(total=Sum('amount'))
    chart_data = [{'label': e['title'], 'value': float(e['total'])} for e in category_totals]

    daily_totals = expenses_qs.annotate(day=TruncDate('date')).values('day').annotate(total=Sum('amount')).order_by('day')
    daily_labels = [d['day'].strftime('%Y-%m-%d') for d in daily_totals]
    daily_values = [float(d['total']) for d in daily_totals]

    monthly_totals = expenses_qs.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')
    month_labels = [m['month'].strftime('%B %Y') for m in monthly_totals]
    month_values = [float(m['total']) for m in monthly_totals]

    context = {
        'expenses': expenses_qs,
        'income_total': income_total,
        'expense_total': expense_total,
        'remaining': remaining,
        'chart_data': chart_data,
        'daily_labels': daily_labels,
        'daily_values': daily_values,
        'month_labels': month_labels,
        'month_values': month_values,
        'income_form': income_form,
        'start_date': start_date,
        'end_date': end_date,
        'expense_labels': [e['label'] for e in chart_data],
        'expense_values': [e['value'] for e in chart_data],
        'pie_labels': [e['label'] for e in chart_data],
        'pie_values': [e['value'] for e in chart_data],
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard:dashboard')
    else:
        form = ExpenseForm()

    return render(request, 'dashboard/add_expense.html', {'form': form})


@login_required
def export_pdf(request):
    expenses = Expense.objects.filter(user=request.user)
    income_total = Income.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    expense_total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    remaining = income_total - expense_total

    # Pie chart data
    category_totals = expenses.values('title').annotate(total=Sum('amount'))
    labels = [c['title'] for c in category_totals]
    sizes = [float(c['total']) for c in category_totals]

    # Pie chart
    fig1, ax1 = plt.subplots(figsize=(5, 5))
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    pie_buffer = BytesIO()
    plt.savefig(pie_buffer, format='png')
    plt.close(fig1)
    pie_buffer.seek(0)
    pie_chart_base64 = base64.b64encode(pie_buffer.read()).decode('utf-8')

    # Monthly bar chart data
    monthly_totals = expenses.annotate(month=TruncMonth('date')) \
                             .values('month') \
                             .annotate(total=Sum('amount')) \
                             .order_by('month')
    months = [m['month'].strftime('%b %Y') for m in monthly_totals]
    monthly_values = [float(m['total']) for m in monthly_totals]

    # Monthly bar chart (thin bar)
    fig, ax = plt.subplots(figsize=(4, 2.5))
    positions = range(len(months))
    bar_width = 0.1  # Make bar thinner

    ax.bar(positions, monthly_values, width=bar_width, color='#2980b9')
    ax.set_title('Monthly Expenses', fontsize=10)
    ax.set_ylabel('Amount (Rs)', fontsize=9)
    ax.set_xticks(positions)
    ax.set_xticklabels(months, rotation=45, ha='right', fontsize=8)
    ax.tick_params(axis='y', labelsize=8)

    plt.subplots_adjust(left=0.15, right=0.95, top=0.85, bottom=0.25)
    plt.tight_layout(pad=1.0)

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    buf.seek(0)
    bar_chart_base64 = base64.b64encode(buf.read()).decode('utf-8')

    context = {
        'expenses': expenses,
        'income_total': income_total,
        'expense_total': expense_total,
        'remaining': remaining,
        'pie_chart_base64': pie_chart_base64,
        'bar_chart_base64': bar_chart_base64,
    }

    html_string = render_to_string('dashboard/report_template.html', context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=dashboard_report.pdf'
        return response
    else:
        return HttpResponse("Error generating PDF", status=500)
