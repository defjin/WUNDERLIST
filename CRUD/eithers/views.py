from django.shortcuts import render, redirect
from .models import Question, Answer

# Create your views here.
def index(request):
    ctx = {
        'questions': Question.objects.all()
    }
    return render(request, 'eithers/index.html', ctx)

def new(request):
    return render(request, 'eithers/new.html')

def create(request):
    title = request.POST.get('title')
    issue_a = request.POST.get('issue_a')
    issue_b = request.POST.get('issue_b')
    image_a = request.FILES.get('image_a')
    image_b = request.FILES.get('image_b')
    question = Question(title=title, issue_a=issue_a,issue_b=issue_b,image_a=image_a,image_b=image_b)
    question.save()

    return redirect('home')

def detail(request, pk):
    question = Question.objects.get(id=pk)
    answers = question.answer_set.all()
    ctx = {
        'question': question,
        'answers': answers,
    }

    return render(request,'eithers/detail.html', ctx)

def answers_create(request, pk):
    pick
    answer = Answer(pick=)
    answers = question.answer_set.all()
    ctx = {
        'question': question,
        'answers': answers,
    }
    return render(request,'eithers/detail.html',ctx)

def ansers_delete(request, pk):
    question = Question.objects.get(id=pk)
    answers = question.answer_set.all()
    ctx = {
        'question': question,
        'answers': answers,
    }
    return render(request,'eithers/detail.html',ctx)