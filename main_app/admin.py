from django.contrib import admin
from .models import Corgi, Feeding, Toy, Photo

# Register your models here.
admin.site.register(Corgi)
admin.site.register(Feeding)
admin.site.register(Toy)
admin.site.register(Photo)
