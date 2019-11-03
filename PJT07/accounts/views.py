from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import CustomUserChangeForm, CustomUserCreationForm

# Create your views here.
def index(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'accounts/index.html', context)

def detail(request, account_pk):
    pass

def create(request):
    if request.method == 'POST': 
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/create.html', context)

def login(request):
    pass

def logout(request):
    pass