from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from IPython import embed
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        # embed()
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = UserCreationForm()
    ctx = {
        'form':form,
    }
    return render(request, 'accounts/auth_form.html',ctx)

# rud는 모두 로그인이 된 이후에 진행해야한다.

def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # 제작의 수준 때문에, 모듈로 사용하는 것을 권한다.
            # username = request.POST.get('username')
            # user = User.objects.get(username=username)
            # if user:
            #     if user.password == request.POST.get('password'):
            #         # 로그인 시킨다 = 세션을 생성한다.
            # else:
            #     # 해킹의 위험때문에 아이디나 패스워드가 틀린 것을 체크하지 않고 뭉뚱그려
            #     # 얘기한다.
            #     # 해당하는 사용자가 없습니다.
            return redirect(request.GET.get('next') or 'articles:index')
    else:
        form = AuthenticationForm()
    ctx = {
        'form':form,
    }
    return render(request, 'accounts/auth_form.html',ctx)    

def logout(request):
    auth_logout(request)
    return redirect('articles:index')
    #if request.method 

@require_POST
def delete(request):
    # DB에서 유저 삭제
    request.user.delete()
    return redirect('articles:index')

@login_required
def update(request):
    #회원정보 수정 로직
    if request.method == 'POST':
        # 실제db
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('articles:index')
    else:
        # 편집화면
        form = CustomUserChangeForm(instance=request.user)
        #폼을 맞춰서 수정하자.
        ctx = {
            'form':form,
        }
        return render(request, 'accounts/auth_form.html',ctx)

@login_required
def change_password(request):
    #비밀번호 수정은 독립되어 있음 
    if request.method == 'POST':
        # 실제 비번 변경
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
        return redirect('articles:index')
    else:
        # 편집화면
        form = PasswordChangeForm(request.user)
        #폼을 맞춰서 수정하자.
        ctx = {
            'form':form,
        }
        return render(request, 'accounts/auth_form.html', ctx)
