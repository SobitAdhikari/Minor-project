# Updated settings/views.py to work without custom_auth.forms

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import DashboardSettings

@login_required
def settings_home(request):
    settings, _ = DashboardSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        settings.dashboard_enabled = not settings.dashboard_enabled
        settings.save()
        return redirect('settings:settings_home')

    return render(request, 'settings/settings_home.html', {'settings': settings})


@login_required
def about_view(request):
    return render(request, 'settings/about.html')


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate

@login_required
def profile_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        user = request.user
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
        else:
            if username:
                user.username = username
            if new_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)
            user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('settings:profile')
    return render(request, 'settings/profile.html')



@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('settings:profile')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'settings/change_password.html', {'form': form})


