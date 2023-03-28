from django.shortcuts import render
from .models import Corgi


# This is temp for corgi data
# corgis = [
#     {'name': 'Clem', 'breed': 'corgi/aussie',
#         'description': 'furry little demon', 'age': 8},
#     {'name': 'Reese', 'breed': 'corgi/aussie',
#         'description': 'gentle and loving', 'age': 6},
#     {'name': 'Buddy', 'breed': 'Welsh Corgi Pembroke',
#         'description': 'Loves belly rubs and playing fetch', 'age': 5},
#     {'name': 'Luna', 'breed': 'Cardigan Welsh Corgi',
#         'description': 'Loves long walks and cuddling', 'age': 2},
#     {'name': 'Milo', 'breed': 'Corgi/Australian Shepherd mix',
#         'description': 'Energetic and playful', 'age': 1},
# ]

# c = Corgi(name="Biscuit", breed='Sphinx', description='Evil looking cuddle monster. Hairless', age=2)
# r = Corgi(name='Reese', breed='aussie/corgi',
#           description='Sweet little guy, gentle and loving', age=6)
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
