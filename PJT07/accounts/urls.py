from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:account_pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]