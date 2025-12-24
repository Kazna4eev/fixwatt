from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list') # Redirect to home page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    orders = request.user.orders.all()

    context = {
        'u_form': u_form,
        'orders': orders
    }

    return render(request, 'accounts/profile.html', context)
