from django.shortcuts import render, redirect, get_object_or_404
from .models import Post

# Create your views here.
def index(request):
    ctx = {
        'posts': Post.objects.all(),
    }
    return render(request, 'posts/index.html', ctx)


def create(request):
    if request.method == 'POST':
        post = Post()
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('posts:index')
    else:
        return render(request,'posts/create.html')

def detail(request, pk):
    ctx = {
        'post': Post.objects.get(id=pk),
    }
    return render(request, 'posts/detail.html', ctx)

def update(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('posts:index')
    else:
        ctx = {
            'post': post
        }
        return render(request, 'posts/update.html', ctx)

def delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('posts:index')




