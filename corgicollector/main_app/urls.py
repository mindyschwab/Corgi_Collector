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
    path('corgis/<int:corgi_id>/add_feeding/',
         views.add_feeding, name='add_feeding'),
    path('corgis/<int:corgi_id>/assoc_toy/<int:toy_id>/',
         views.assoc_toy, name='assoc_toy'),
    path('corgis/<int:corgi_id>/remove_toy/<int:toy_id>/',
         views.remove_toy, name='remove_toy'),
    path('toys/', views.ToyList.as_view(), name='toys_index'),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
]
