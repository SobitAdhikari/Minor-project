from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view,name='dashboard'),
    # path('add-income/', views.add_income, name='add_income'),
    path('add-expense/', views.add_expense, name='add_expense'),  # Add this line
    path('export-pdf/', views.export_pdf, name='export_pdf'),

]
