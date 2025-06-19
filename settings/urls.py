from django.urls import path
from . import views

app_name = 'settings_app'

urlpatterns = [
    path('', views.settings_home, name='settings_home'),
    path('about/', views.about_view, name='about'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
]
