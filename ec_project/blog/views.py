from django.shortcuts import render


def landing(request):
    return render(request, 'blog/landing.html')

def notes(request):
    return render(request, 'blog/notes.html')

def homeworks(request):
    return render(request, 'blog/homeworks.html')

def learning(request):
    return render(request, 'blog/learning.html')
