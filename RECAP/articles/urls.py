from django.urls import path
from .import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:article_pk>/', views.detail, name='detail'),
    path('create/', views.create, name="create"),
    path('<int:article_pk>/delete/', views.delete, name='delete'),
    path('<int:article_pk>/update/', views.update, name='update'),
    path('<int:article_pk>/comment/', views.create_comment, name='create_comment'),
    path('send_cookie', views.send_cookie, name='send'),
    path('<int:article_pk>/like/', views.like, name='like'),
    path('explore/', views.explore, name='explore'),
    path('tags/', views.tags, name='tags'),
    path('hashtag/<int:hashtag_pk>', views.hashtag, name='hashtag'),
]