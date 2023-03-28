from django.urls import path
from . import views

urlpatterns = [
    # defining the root route (path, view, name(optional, kwarg)
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('corgis/', views.corgis_index, name='index'),
    path('corgis/<int:corgi_id>/', views.corgis_detail, name='detail'),
]
