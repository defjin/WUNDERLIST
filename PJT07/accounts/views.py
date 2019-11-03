from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    persons = get_user_model().objects.all()
    context = {
        'persons': persons,
    }
    return render(request, 'accounts/index.html', context)

def detail(request, account_pk):
    person = get_object_or_404(get_user_model(), pk=account_pk)
    make_reviews  = person.review_set.all()
    movies = person.like_movies.all()

    context = {
        'person': person,
        'make_reviews' : make_reviews,
        'movies' : movies,
    }
    return render(request, 'accounts/detail.html', context)

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
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'accounts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/auth_form.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:index')

@login_required
def follow(request, person_pk):
    person = get_object_or_404(get_user_model(), pk=person_pk)
    user = request.user

    if person.followers.filter(pk=user.pk).exists():
        person.followers.remove(user)
    else:
        #자기자신 follow 막기
        person.followers.add(user)
    return redirect('accounts:detail', person_pk)




