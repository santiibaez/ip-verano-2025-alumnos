# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services.services import getAllImages # Importar la función getAllImages
from .layers.services.services import filterByCharacter, filterByHouse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .layers.services.services import getAllFavourites, saveFavourite, deleteFavourite
from .layers.services import services



def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = getAllImages()
    favourite_list = getAllFavourites(request)

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')
    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        images = filterByCharacter(name)
        favourite_list = getAllFavourites(request)
        #creamos nueva lista para guardar solo las coincidencias
        #Recorremos cada imagen hasta encontrar coincidencias      
        #Devolvemos la lissta con las coincidencias        
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# función utilizada para filtrar por casa Gryffindor o Slytherin.
def filter_by_house(request):
    house = request.POST.get('house', '')

    if house != '':
        images = filterByHouse(house) # debe traer un listado filtrado de imágenes, según la casa.
        favourite_list = getAllFavourites(request)

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    services.saveFavourite(request)
    return redirect('home')

@login_required
def deleteFavourite(request):
    services.deleteFavourite(request)
    return redirect('favoritos')

@login_required
def exit(request):
    logout(request)
    return redirect('home')

#traemos las funciones necesarias y cambiamos los pass por los return para que las funciones devuelvan algo