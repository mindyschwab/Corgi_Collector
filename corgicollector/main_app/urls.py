from django.urls import path
from . import views

urlpatterns = [
    # defining the root route (path, view, name(optional, kwarg)
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('corgis/', views.corgis_index, name='index'),
    path('corgis/<int:corgi_id>/', views.corgis_detail, name='detail'),
    path('corgis/create/', views.CorgiCreate.as_view(), name='corgis_create'),
    path('corgis/<int:pk>/update/',
         views.CorgiUpdate.as_view(), name='corgis_update'),
    path('corgis/<int:pk>/delete/',
         views.CorgiDelete.as_view(), name='corgis_delete'),
]
