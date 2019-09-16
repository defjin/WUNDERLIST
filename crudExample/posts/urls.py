from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/create_comment/', views.create_comment),
]