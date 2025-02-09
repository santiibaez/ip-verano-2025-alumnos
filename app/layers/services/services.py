# capa de servicio/lógica de negocio
#from ..transport import transport 
import random
from ..transport import transport
from ..persistence import repositories
from ..utilities.translator import fromRequestIntoCard, fromRepositoryIntoCard, fromTemplateIntoCard
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de HP.
def getAllImages():
    # debe ejecutar los siguientes pasos:
    # 1) traer un listado de imágenes crudas desde la API (ver transport.py)
    raw_images = transport.getAllImages()
    # 2) convertir cada img. en una card.
    cards = []
    for image in raw_images:
        # Mostramos los nombres alternativos si es que hay
        if image['alternate_names']:
            alternate_name = random.choice(image['alternate_names'])
        else:
            alternate_name = "Nombre alternativo no disponible"
        # Crear una card con la información de la imagen
        card = fromRequestIntoCard({
            'name': image['name'],
            'gender': image['gender'],
            'house': image.get('house'),
            'alternate_names': alternate_name,
            'actor': image.get('actor'),
            'image': image['image']
        })
        cards.append(card)
    # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas.
    return cards
    # ATENCIÓN: contemplar que los nombres alternativos, para cada personaje, deben elegirse al azar. Si no existen nombres alternativos, debe mostrar un mensaje adecuado.
    #pass

# función que filtra según el nombre del personaje.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():
        # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.
        if (name.lower() in card.name.lower()): 
            filtered_cards.append(card)

    return filtered_cards

# función que filtra las cards según su casa.
def filterByHouse(house_name):
    filtered_cards = []

    for card in getAllImages():
        # debe verificar si la casa de la card coincide con la recibida por parámetro. Si es así, se añade al listado de filtered_cards.
        if (house_name.lower() in card.house.lower()): #es igual al filterByCharacter
            filtered_cards.append(card)

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = fromTemplateIntoCard(request) # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = repositories.get_all_favourites(user) # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = fromRepositoryIntoCard(favourite) # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID