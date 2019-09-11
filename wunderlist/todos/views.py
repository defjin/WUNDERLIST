from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo

# Create your views here.
def index(request):
    todos = Todo.objects.all()
    ctx = {
        'todos':todos,
    }
    return render(request, 'todos/index.html', ctx)

def create(request):
    # new와 create를 통합
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due-date')
        
        Todo.objects.create(title=title, due_date =due_date)
        return redirect('todos:index')
    else:
        return render(request, 'todos/create.html')
        

def update(request, pk):
    todo = get_object_or_404(Todo, id=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due-date')
        todo.title = title
        todo.due_date = due_date
        todo.save()
        return redirect('todos:index')
    else:
        ctx = {
            'todo':todo,
        }
        return render(request, 'todos/update.html', ctx)

def delete(reqeust, pk):
    todo = get_object_or_404(Todo, id=pk)
    todo.delete()
    return redirect('todos:index')