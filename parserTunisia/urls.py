from django.urls import path
from . import views



urlpatterns = [
path('<categorie>/<tab>', views.manage, name='manage'),
path('<categorie>/<tab>/welcome', views.redirection, name='redirection'),
path('manageTravel/manage/<manage>', views.redirection1, name='redirection1'),


path('<categorie>/<tab>/all', views.show, name='show'),
path('<categorie>/<tab>/<o>', views.showListe, name=''),
path('<categorie>/<tab>/<keyword>/<showKeywordbord>', views.showBord, name='showBord'),
path('<categorie>/<filter>/<tab>/<keyword>/', views.showFilter, name='showFilter'),
path('<categorie>/<tab>/<keyword>/<name>/<c>', views.showDetails, name='showDetails'),
path('<categorie>/<tab>/<keyword>/<typeBien>/<name>/<c>', views.showDetails1, name='showDetails1'),

 ]
