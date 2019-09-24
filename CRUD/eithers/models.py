from django.db import models

# Create your models here.
class Question(models.Model):
    title = models.TextField()
    issue_a = models.TextField()
    issue_b = models.TextField()
    image_a = models.ImageField()
    image_b = models.ImageField()

    class Meta:
        ordering = ['-pk']


class Answer(models.Model):
    pick = models.IntegerField()
    comment = models.TextField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pk']
