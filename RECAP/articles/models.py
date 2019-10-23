from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
class Hashtag(models.Model):
    content = models.TextField(unique=True)


class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles', blank=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pk',)

    #method도 추가예정
    def get_absolute_url(self):
        #return reverse('어디로가야하죠', '인자')
        return reverse('articles:detail', kwargs={'article_pk': self.pk})

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.content
