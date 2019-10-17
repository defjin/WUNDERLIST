from django.shortcuts import render, redirect, get_object_or_404, Http404
from .models import Article
from .forms import ArticleForm, CommentForm
from IPython import embed
# django.http import Http404
from django.views.decorators.http import require_http_methods, require_POST

# Create your views here.
def index(request):
    ctx = {
        'articles': Article.objects.all(),
    }
    return render(request, 'articles/index.html', ctx)

def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    # 만약 Article에서 pk를 찾았을 때 error가 나오면 error handling 하기
    # try:
    #     article = Article.objects.get(pk=article_pk)
    # except Article.DoesNotExist:
    #     raise Http404('어딜 가니? 해당하는 id의 글이 없잖아')
    comment_form = CommentForm()
    ctx = {
        'article': article,
        'comment_form': comment_form,
        'comments': article.comment_set.all(),
    }
    return render(request, 'articles/detail.html', ctx)


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
        embed()
        if form.is_valid():
            #title = form.cleaned_data.get('title')
            #content = form.cleaned_data.get('content')
            #new_article = Article.objects.create(title=title, content=content)
            new_article = form.save()
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

# update -> articles/:id/update |  (put) articles/:id
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        #실제 DB의 데이터를 수정
        form = ArticleForm(request.POST, instance=article) # 인자가 하나면 modelform에서는 create로 인식하게 됨
        if form.is_valid():
            # form을 사용할 때
            # article.title = form.cleaned_data.get('title')
            # article.content = form.cleaned_data.get('content')
            # article.save()
            # modelform을 사용할 때
            article = form.save() #이거 하게 되면 데이터가 계속 새로 생성되어서 추가됨
            return redirect(article)
    
    # 편집화면
    # form
    # form = ArticleForm(
    #     initial={
    #         'title': article.title,
    #         'content' : article.content,
    # })
    #model form
    form = ArticleForm(instance=article)
    ctx = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/update.html', ctx)
        

# Delete -> articles/:id/delete
# 뷰 데코레이터를 사용하면 완전히 채워넣을 수 있음 - 특정양식으로는 절대 들어올 수 없도록
# view decorator  : http405 error : allowed http methods 관련된 양식 
# 잘못된 접근입니다 !!
@require_POST
def delete(request, article_pk):
    # 기본적인 get 형태 - url이 노출되어서 삭제의 위험이 있음
    #article = get_object_or_404(Article, pk=article_pk)
    #article.delete()
    # POST - 수정이나 삭제는 반드시 post로
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        article.delete()
        return redirect('articles:index')
    else:
        return redirect(article)


##### TODO
# Comment 생성 삭제
# -POST /articles/:id/comments
# -POST /articles/:id/comments_delete/:c_id
# modelform 사용하기
def create_comment(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            # commit : database commit, 실제 db에 저장한다 
            #embed()
            # comment.article : 객체를 리턴함
            # 1번
            #comment.article_id = article_pk
            #comment.save()
            # return redirect('articles:detail',article_pk)
            # 2번
            comment.article = article
            comment.save()
        return redirect(article)

            
            

        


    return render(request, 'articles/update.html', ctx)