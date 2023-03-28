from django.shortcuts import render
from .models import Corgi

# Create your views here.

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def corgis_index(request):
    corgis = Corgi.objects.all()
    return render(request, 'corgis/index.html', {
        'corgis': corgis
    })


def corgis_detail(request, corgi_id):
    corgi = Corgi.objects.get(id=corgi_id)
    return render(request, 'corgis/detail.html', {
        'corgi': corgi
    })
