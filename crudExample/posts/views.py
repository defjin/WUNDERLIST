from django.shortcuts import render, redirect
from .models import Post, Comment

# Create your views here.
def index(request):
    # table 형태로 게시판을 보여줌
    posts = Post.objects.all()

    context = {
        'posts': posts
    }
    return render(request, 'posts/index.html', context)

def create(request):
    if request.method == 'POST':
        Post.objects.create(
            title = request.POST.get('title'), 
            content = request.POST.get('content'),
            image = request.FILES.get('image'),
        )
        return redirect('home')
    else:
        return render(request, 'posts/new.html')


def detail(request, pk):
    # pk라는 id를 가진 글을 찾아와 보여줌
    post = Post.objects.get(pk=pk)

    # 해당 글에 달려있는 모든 댓글을 보여줌
    comments = post.comment_set.all()

    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'posts/detail.html', context)

def delete(request, pk):
    # pk라는 id를 가진 글을 삭제
    post = Post.objects.get(pk=pk)
    post.delete()

    return redirect('home')

def update(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.image = request.FILES.get('image')
        post.save()

        return redirect('posts:detail', pk)
    else:
        context = {
            'post': post,
        }
        return render(request, 'posts/update.html', context)

def create_comment(request, pk):
    # 댓글 작성, 디테일 페이지로 리다이렉트
    Comment.objects.create(
        content=request.GET.get('content'),
        post=Post.objects.get(pk=pk)
    )
    return redirect('posts:detail', pk)