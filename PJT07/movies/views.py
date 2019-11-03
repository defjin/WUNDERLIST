from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Genre, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    ctx = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', ctx)

def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review_Form = ReviewForm()

    ctx = {
        'movie': movie,
        'reviews': movie.review_set.all(),
        'review_Form' : review_Form,
    }
    return render(request, 'movies/detail.html', ctx)

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

@require_POST
@login_required
def delete_review(request, movie_pk, review_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        review = get_object_or_404(Review, pk=review_pk)
        if request.user == review.user:
            review.delete()
    return redirect('movies:detail', movie_pk) 
    
@login_required
def like(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    user = request.user
    if movie.like_users.filter(pk=user.pk).exists(): #(2)
        movie.like_users.remove(user)
    else:
        movie.like_users.add(user)
    return redirect('movies:detail', movie_pk)