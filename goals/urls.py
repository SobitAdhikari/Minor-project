from django.urls import path
from . import views

app_name = 'goals'

urlpatterns = [
    path('', views.goal_list, name='goal_list'),
    path('add/', views.add_goal, name='add_goal'),
    path('edit/<int:pk>/', views.GoalUpdateView.as_view(), name='goal_update'),
    path('delete/<int:pk>/', views.GoalDeleteView.as_view(), name='goal_delete'),
    path('add-savings/<int:pk>/', views.add_savings, name='add_savings'),
]

