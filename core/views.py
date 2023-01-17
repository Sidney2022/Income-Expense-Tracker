from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def exp(request):
    return render(request, 'expenses/index.html')

