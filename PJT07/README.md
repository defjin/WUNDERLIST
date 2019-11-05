# Project07_README

## 1. 목표

- 협업을 통한 데이터베이스 모델링 및 기능 구현
- 다양한 형태의 데이터베이스 관계 설정



## 2. 기능

### 데이터베이스 설계

- accounts_users: id, username, password, email, firsr_name, last_name

- movies_movies: id, title, audience, poster_url, description, genre_id

- movies_genres: id, name

- movies_reviews: id, content, score, movie_id, user_id

- movies_like_movies_user: id, user_id, movie_id

- ```python
  from django.db import models
  from django.contrib.auth.models import AbstractUser
  from django.conf import settings
  
  # Create your models here.
  class CustomUser(AbstractUser):
      followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings', blank=True)
  ```

- ```python
  from django.db import models
  from django.conf import settings
  
  # Create your models here.
  class Genre(models.Model):
      name = models.CharField(max_length=30)
  
  class Movie(models.Model):
      title = models.CharField(max_length=50)
      audience = models.IntegerField()
      poster_url = models.CharField(max_length=200)
      description = models.TextField()
      genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
      like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies', blank=True)
  
  class Review(models.Model):
      content = models.CharField(max_length=200)
      score = models.IntegerField()
      movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
      user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  ```

### Seed Data 반영

- python manage.py loaddata genre.json

- python manage.py loaddata movie.json

- admin.py

  ```python
  from django.contrib import admin
  from .models import Movie, Genre
  
  # Register your models here.
  class MovieAdmin(admin.ModelAdmin):
      list_display = ('pk', 'title', 'audience', 'poster_url', 'description')
      
  admin.site.register(Movie, MovieAdmin)
  
  class GenreAdmin(admin.ModelAdmin):
      list_display = ('pk', 'name')
  
  admin.site.register(Genre, GenreAdmin)
  ```

### accounts App

- 회원가입

  ```python
  from django.contrib.auth.forms import UserCreationForm
  from .forms import CustomUserCreationForm
  
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
  
  ```

  ```html
  {% extends 'base.html' %}
  
  {% block body %}
      <form action="{% url 'accounts:create' %}" method='POST'>
          {% csrf_token %}
          {{ form.as_p }}
          <input type="submit">
      </form>
      
  {% endblock %}
  ```

- 로그인

  ```python
  from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
  
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
  ```

  ```html
  {% extends 'base.html' %}
  {% block body %}
      <form action="{% url 'accounts:login' %}" method="POST">
          {% csrf_token %}
          {{ form.as_p }}
          <input type="submit">
      </form>
  {% endblock %}
  ```

- 로그아웃

  ```python
  @login_required
  def logout(request):
      auth_logout(request)
      return redirect('accounts:index')
  ```

- 유저 목록

  ```python
  from django.contrib.auth import get_user_model
  
  def index(request):
      persons = get_user_model().objects.all()
      context = {
          'persons': persons,
      }
      return render(request, 'accounts/index.html', context)
  ```

  ```html
  {% extends 'base.html' %}
  
  {% block body %}
  
  {% for person in persons %}
    <p><a href="{% url 'accounts:detail' person.pk %}">{{ person.username }}</a></p>
  
  {% endfor %}
  
  {% endblock %}
  ```

- 유저 상세보기

  ```python
  from django.shortcuts import get_object_or_404
  
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
  ```

  ```html
  {% extends 'base.html' %}
  
  {% block body %}
  <h1>{{ person }}</h1>
  {% with followers=person.followers.all followings=person.followings.all %}
    {% if user != person %}
      {% if user in followers %}
        <a class="btn btn-outline-primary" href="{% url 'accounts:follow' person.pk %}">언팔로우</a>
      {% else %}
        <a class="btn btn-primary" href="{% url 'accounts:follow' person.pk %}">팔로우</a>
      {% endif %}
    {% endif %}
    <p>팔로워수 : {{ followers | length }} </p>
    <p>
      팔로워 : 
      {% for follower in followers %} 
        {{ follower }}
      {% endfor %}
    </p>
    <p>팔로잉수 : {{ person.followings.count }}</p>
    <p>
      팔로잉 : 
      {% for following in followings %} 
        {{ following }}
      {% endfor %}
    </p>
  {% endwith %}
  <hr>
  <h2> {{ person }}가 쓴 리뷰</h2>
  {% with reviews=person.review_set.all %}
    {% for review in reviews %}
    <p>
      내용 : {{ review.content }} | 
      점수 : {{ review.score }} |
    </p>
    {% endfor %}
  {% endwith %}
  
  <h2> {{ person }}가 좋아하는 영화</h2>
    {% for movie in person.like_movies.all %}
      {{ movie.title }}
    {% endfor %}
  {% endblock %}
  ```

### movies App

- 영화 목록

  ```python
  from .models import Movie, Genre, Review
  
  def index(request):
      movies = Movie.objects.all()
      ctx = {
          'movies': movies,
      }
      return render(request, 'movies/index.html', ctx)
  ```

  ```html
  {% extends 'base.html' %}
  
  {% block body %}
      {% for movie in movies %}
          <p>{{ movie.title }}</p>
          <p><a href="{% url 'movies:detail' movie.pk %}"><img height='100px' width='100px' src="{{ movie.poster_url }}" alt="{{ movie.title }}"></a></p>
      {% endfor %}
  
  
  {% endblock %}
  ```

- 영화 상세보기

  ```python
  from django.shortcuts import render, get_object_or_404, redirect
  from .forms import ReviewForm
  
  def detail(request, movie_pk):
      movie = get_object_or_404(Movie, pk=movie_pk)
      review_Form = ReviewForm()
  
      ctx = {
          'movie': movie,
          'reviews': movie.review_set.all(),
          'review_Form' : review_Form,
      }
      return render(request, 'movies/detail.html', ctx)
  ```

  ```html
  {% extends 'base.html' %}
  
  {% block body %}
      <p>영화명: {{ movie.title }}</p>
      <p>누적관객수: {{ movie.audience }}</p>
      <p>포스터 이미지 URL: {{ movie.poster_url }}</p>
      <p>영화소개: {{ movie.description }}</p>
      {% if user.is_authenticated %}
         <form action="{% url 'movies:create_review' movie.pk %}" method='POST'>
             {% csrf_token %}
              {{ review_Form }}
              <input type="submit">
          </form>
          
      {% endif %}
  
      <h2>좋아요 목록 </h2>
      <p>좋아요 : {{ movie.like_users.count  }}</p>
      {% with likers=movie.like_users.all %}
        <p>좋아요 목록 : 
          {% for u in likers %}
            {{ u }}
          {% endfor %}
        </p>
        {% if user in likers %}
          <a href="{% url 'movies:like' movie.pk %}">좋아요 취소</a>
        {% else %}
          <a href="{% url 'movies:like' movie.pk %}">좋아요!</a>
        {% endif %}
      {% endwith %}
  
      {% for review in reviews %}
          <p>{{ review.content }} {{ review.score }} {{ review.user }} {{ review.movie.title }}</p>
          <form action="{% url 'movies:delete_review' movie.pk review.pk  %}" method='POST'>
                  {% csrf_token %}
              <input type="submit" value="삭제">
          </form>
      {% endfor %}
  
  {% endblock %}
  ```

- 평점 생성

  ```python
  @login_required
  def create_review(request, movie_pk):
      movie = get_object_or_404(Movie, pk=movie_pk)
  
      if request.method == 'POST':
          form = ReviewForm(request.POST)
          if form.is_valid():
              review = form.save(commit=False)
              review.movie = movie
              review.user = request.user
              review.save()
      
      return redirect('movies:detail', movie_pk)
  ```

- 평점 삭제

  ```python
  @require_POST
  @login_required
  def delete_review(request, movie_pk, review_pk):
      if request.user.is_authenticated:
          movie = get_object_or_404(Movie, pk=movie_pk)
          review = get_object_or_404(Review, pk=review_pk)
          if request.user == review.user:
              review.delete()
      return redirect('movies:detail', movie_pk) 
  ```

- 영화 좋아요 기능 구현

  ```python
  @login_required
  def like(request, movie_pk):
      movie = Movie.objects.get(pk=movie_pk)
      user = request.user
      if movie.like_users.filter(pk=user.pk).exists(): #(2)
          movie.like_users.remove(user)
      else:
          movie.like_users.add(user)
      return redirect('movies:detail', movie_pk)
  ```



### 느낀점

- 남에게 navigating 을 하는 과정에서 제가 잘 모르는 부분에 대해서 다시 한 번 생각할 수 있는 계기가 된 것 같습니다. 
   또 driver로 남이 말해주는 것을 그대로 치면서 짝이 잘 알고 있는 부분과, 잘 모르는 부분도 확실히 알 수 있었습니다. 
- 다만, 확실히 잘 안다면, 혼자 짜는 것이 훨씬 빠를 것이지만, 지식을 전수하는 측면이라면 상당히 도움이 될 것 같습니다

- 제가 잘 몰랐던 부분에 대해서는 팀원에게 도움을 받고, 팀원이 모르는 부분은 제가 알려주면서 페어 프로그래밍을 경험해 볼 수 있었습니다
- 이 과정 속에서 같은 문제에 대한 다른 접근 방식, 사고 과정을 가져볼 수 있었고, 접근 방식이 같아도 코드가 조금씩은 달랐는데, 코드의 효율성, 가독성 등에 대해서도 고민해 볼 수 있었습니다