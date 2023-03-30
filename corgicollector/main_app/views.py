from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Corgi, Toy
from .forms import FeedingForm

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
    # creating a list of theids of all the toys that are associated with the corgi
    id_list = corgi.toys.all().values_list('id')
    toys_corgi_doesnt_have = Toy.objects.exclude(id__in=id_list)
    feeding_form = FeedingForm()
    return render(request, 'corgis/detail.html', {
        'corgi': corgi,
        'feeding_form': feeding_form,
        'toys': toys_corgi_doesnt_have
    })


class CorgiCreate(CreateView):
    model = Corgi
    fields = ['name', 'breed', 'description', 'age']


class CorgiUpdate(UpdateView):
    model = Corgi
    fields = ['breed', 'description', 'age']


class CorgiDelete(DeleteView):
    model = Corgi
    success_url = '/corgis/'


def add_feeding(request, corgi_id):
    # create a ModelForm instance using the data in request.POST
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the corgi_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.corgi_id = corgi_id
        new_feeding.save()
    return redirect('detail', corgi_id=corgi_id)


class ToyList(ListView):
    model = Toy


class ToyDetail(DetailView):
    model = Toy


class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'


class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']


class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'


def assoc_toy(request, corgi_id, toy_id):
    Corgi.objects.get(id=corgi_id).toys.add(toy_id)
    return redirect('detail', corgi_id=corgi_id)


def remove_toy(request, corgi_id, toy_id):
    Corgi.objects.get(id=corgi_id).toys.remove(toy_id)
    return redirect('detail', corgi_id=corgi_id)
