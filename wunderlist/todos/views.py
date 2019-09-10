from django.shortcuts import render, redirect
from .models import Todo

# Create your views here.
def index(request):
    todos = Todo.objects.all()
    ctx = {
        'todos':todos,
    }
    return render(request, 'todos/index.html', ctx)

def new(request):
    return render(request, 'todos/new.html')

def create(request):
    title = request.POST.get('title')
    due_date = request.POST.get('due-date')
    
    Todo.objects.create(title=title, due_date =due_date)
    return redirect('todos:index')

def edit(request, pk):
    todo = Todo.objects.get(id=pk)
    ctx = {
        'todo':todo,
    }
    return render(request, 'todos/edit.html', ctx)

def update(request, pk):
    title = request.POST.get('title')
    due_date = request.POST.get('due-date')

    todo = Todo.objects.get(id=pk)
    todo.title = title
    todo.due_date = due_date
    todo.save()
    return redirect('todos:index')

def delete(reqeust, pk):
    todo = Todo.objects.get(id=pk)
    todo.delete()
    return redirect('todos:index')