from django.db import models
from django.urls import reverse

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pk',)

    #method도 추가예정
    def get_absolute_url(self):
        #return reverse('어디로가야하죠', '인자')
        return reverse('articles:detail', kwargs={'article_pk': self.pk})