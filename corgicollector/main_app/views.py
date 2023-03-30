import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Corgi, Toy, Photo
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
    fields = ['name', 'color', 'description']


class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'


def assoc_toy(request, corgi_id, toy_id):
    Corgi.objects.get(id=corgi_id).toys.add(toy_id)
    return redirect('detail', corgi_id=corgi_id)


def remove_toy(request, corgi_id, toy_id):
    Corgi.objects.get(id=corgi_id).toys.remove(toy_id)
    return redirect('detail', corgi_id=corgi_id)


def add_photo(request, corgi_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            # using the slice method to get everything before the. in the file name
        photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, cat_id=cat_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', cat_id=cat_id)
