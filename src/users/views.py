from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account Created Successfully! You Can Now Log In')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def profile_view(request):

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Info Updated Successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile.html', context={'u_form':u_form})