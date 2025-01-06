from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("gene", views.search, name='gene_search'),
    path("blast", views.blast, name='blast'),
    path("blastResult", views.blastResult, name='blastResult'),
    path("insect/<int:id>", views.insect, name='insect'),
    path("compound/<int:id>", views.compound, name='compound'),
    path("gene/<int:id>", views.gene, name='gene'),
    path("compound", views.compoundlist, name='compoundlist'),
    path('insect', views.insectlist, name='insectlist'),
    path('get_insect_content/<int:id>/', views.get_insect_content, name='get_insect_content'),
    path('download', views.download, name='download'),
    path('download_file/<str:file_path>/', views.download_file, name='download_file'),
    path('tree', views.tree, name='tree'),
    path('help', views.help, name='help'),
]
