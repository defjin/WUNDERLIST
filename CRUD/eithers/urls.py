from django.urls import path, include
import eithers.views as views

app_name='eithers'


urlpatterns = [
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('detail/<int:pk>', views.detail, name='detail'),
] 