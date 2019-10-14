from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm

# Create your views here.
def index(request):
    ctx = {
        'articles': Article.objects.all(),
    }
    return render(request, 'articles/index.html', ctx)

def detail(reqeust, article_pk):
    article = Article.objects.get(pk=article_pk)
    ctx = {
        'article': article,
    }
    return render(reqeust, 'articles/detail.html', ctx)

def create(request):
    # GET/POST
    if request.method == 'POST':
        # title = request.POST.get('title')
        # content = request.POST.get('content')
        # new_article = Article.objects.create(
        #     title=title,
        #     content=content,
        # )
        form = ArticleForm(request.POST)
        #is_valid : 제대로된 요청이 아니면 무시해버린다
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            new_article = Article.objects.create(title=title, content=content)
            # 전송된 데이터의 유효성 검사
            # redirect : 객체가 들어왔을 때는 get_absolute_url이 있는지를 살펴보고 그대로 수행한다.
            return redirect(new_article)
        else:
            return redirect('articles:create')
    else:
        form = ArticleForm()
        ctx = {
            'form' : form,
        }
        return render(request, 'articles/create.html', ctx)
    