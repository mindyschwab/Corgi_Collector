import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Corgi, Toy, Photo
from .forms import FeedingForm


# Create your views here.

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


@login_required
def corgis_index(request):
    corgis = Corgi.objects.filter(user=request.user)
    return render(request, 'corgis/index.html', {
        'corgis': corgis
    })


@login_required
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


class CorgiCreate(LoginRequiredMixin, CreateView):
    model = Corgi
    fields = ['name', 'breed', 'description', 'age']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CorgiUpdate(LoginRequiredMixin, UpdateView):
    model = Corgi
    fields = ['breed', 'description', 'age']


class CorgiDelete(LoginRequiredMixin, DeleteView):
    model = Corgi
    success_url = '/corgis/'


@login_required
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


class ToyList(LoginRequiredMixin, ListView):
    model = Toy


class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy


class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'


class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color', 'description']


class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'


@login_required
def assoc_toy(request, corgi_id, toy_id):
    Corgi.objects.get(id=corgi_id).toys.add(toy_id)
    return redirect('detail', corgi_id=corgi_id)


@login_required
def remove_toy(request, corgi_id, toy_id):
    Corgi.objects.get(id=corgi_id).toys.remove(toy_id)
    return redirect('detail', corgi_id=corgi_id)


@login_required
def add_photo(request, corgi_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        #  using the slice method to get everything after the. in the file name (e.g. .jpg)
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, corgi_id=corgi_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', corgi_id=corgi_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # automaitcally log the user in after signing up
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - please try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
