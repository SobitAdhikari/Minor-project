# For HTML
from django.urls import path
from .views import expense_create_view, expense_list_view , delete_expense_view
app_name = 'expenses'

urlpatterns = []

urlpatterns += [
    path('expenses/create/', expense_create_view, name='create_expense'),
    path('expenses/', expense_list_view, name='list_expenses'),
    path('delete/<int:expense_id>/', delete_expense_view, name='delete_expense'),

]

# for drf
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')

urlpatterns += router.urls

