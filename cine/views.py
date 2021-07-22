from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from datetime import date
from django.core.paginator import Paginator
import io
import os
import requests
from urllib.parse import urlparse
from PIL import Image

# Create your views here.
from .forms import GenreForm, StudioForm, CountryForm
from .models import Studio, Country, Genre, Movie, Actor, Lugar, Biografia, Director, Favourite


# *************************** LOGIN / REGISTRO  *******************


def do_login(request):
    if request.method == "GET":
        return render(request, "accounts/login.html")

    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is None:
        return render(request, "accounts/login.html")

    login(request, user)
    return redirect('index')


def do_logout(request):
    logout(request)
    return redirect('login')


def do_register(request):
    if request.method == "GET":
        return render(request, "accounts/register.html")

    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    User.objects.create_user(username, email, password)

    return redirect('login')


def index(request):
    data = {
        "movies": Movie.objects.all(),
        "genres": Genre.objects.all()
    }
    return render(request, 'index.html', context=data)


def movie_genre_filter(request):
    genres = request.GET.getlist("genres")
    data = {
        "movies": Movie.objects.filter(genres__id__in=genres).distinct(),
        "genres": Genre.objects.all(),
        "genres_filtered": Genre.objects.filter(id__in=genres)
    }
    return render(request, "index.html", context=data)


@login_required
def movie_view(request, id):
    movie = Movie.objects.get(id=id)
    try:
        favourite = Favourite.objects.get(movie_id=movie.id)
    except ObjectDoesNotExist:
        favourite = ''
    data = {
        "movie": movie,
        "genres": movie.genres.all(),
        "persons": movie.actors.all(),
        'favourite': favourite
    }
    return render(request, 'movie/movie-view.html', context=data)


@login_required
def movie_delete(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
        favourite = Favourite.objects.get(movie_id=movie.id)
        os.remove(movie.image.path)
        favourite.delete()
        movie.delete()
        return HttpResponseRedirect("/cine/index")
    except Movie.DoesNotExist:
        return HttpResponseNotFound("Película no encontrada")


@login_required
def movie_load(request, id):
    data = {
        "movie": Movie.objects.get(id=id),
        "countries": Country.objects.all(),
        "studios": Studio.objects.all(),
        "genres": Genre.objects.all(),
        "persons": Actor.objects.all(),
        "directors": Director.objects.all()
    }
    return render(request, "movie/movie-detail.html", context=data)


@login_required
def movie_new(request):
    data = {
        "countries": Country.objects.all(),
        "studios": Studio.objects.all(),
        "genres": Genre.objects.all(),
        "persons": Actor.objects.all(),
        "directors": Director.objects.all()
    }
    return render(request, "movie/movie-detail.html", context=data)


@login_required
def movie_save(request):
    creation = not request.POST.get("id")
    director = Director.objects.get(id=int(request.POST.get("director")))

    genres = request.POST.getlist("genres")
    actors = request.POST.getlist("persons")

    country_id_str = request.POST.get("country_id")
    country_id = int(country_id_str) if country_id_str else None

    studio_id_str = request.POST.get("studio_id")
    studio_id = int(studio_id_str) if studio_id_str else None

    if creation:
        image_request = request.FILES.get("image")
        location = 'static/img'
        path = os.path.join(location, str(request.FILES.get('image')))
        if os.path.exists(path):
            os.remove(path)
        if request.POST.get('image_url') != '':
            url = request.POST.get('image_url')
            url_web(url)
            image_request = myimage
        movie = Movie.objects.create(

            name=request.POST.get("name"),
            description=request.POST.get("description"),
            image=image_request,
            cost=int(request.POST.get("cost")),
            income=int(request.POST.get("income")),
            date=request.POST.get("date"),
            country_id=country_id,
            studio_id=studio_id,
            director=director
        )
        movie.genres.set(genres)
        movie.actors.set(actors)

    else:
        # Editar una película existente
        id_movie = int(request.POST.get("id"))
        movie = Movie.objects.get(id=id_movie)

        movie.name = request.POST.get("name")
        movie.description = request.POST.get("description")
        if request.POST.get('image_url') != '':
            url = request.POST.get('image_url')
            url_web(url)
            movie.image = myimage
        else:
            movie.image = request.FILES.get("image")
            movie.cost = int(request.POST.get("cost"))
            movie.income = int(request.POST.get("income"))
            movie.date = request.POST.get("date")
            movie.country_id = country_id
            movie.studio_id = studio_id
            movie.genres.set(genres)
            movie.actors.set(actors)
            movie.director = director

            location = 'static/img'
            path = os.path.join(location, str(request.FILES.get('image')))
            if os.path.exists(path):
                os.remove(path)
            movie.save()
    return HttpResponseRedirect("/cine/movie-view/{}/view".format(movie.id))


def url_web(url):
    global myimage
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    parsed = urlparse(url)
    cadena = parsed.path
    posicion_barra = cadena.rfind('/')
    myimage = cadena[posicion_barra + 1:]
    img.save(os.getcwd() + '/static/img/' + myimage)


@login_required
def movie_detail(request):
    data = {}
    return render(request, 'movie/movie-detail.html', context=data, )


@login_required
def movie_favourite(request, id):
    movie = Movie.objects.get(id=id)
    userID = request.user.id
    favourite = Favourite.objects.create(
        user_id=userID,
        movie_id=movie.id)
    data = {
        "movie": movie,
        "genres": movie.genres.all(),
        "persons": movie.actors.all(),
        'favourite': favourite
    }
    favourite.save()
    return render(request, 'movie/movie-favourite.html', context=data, )


@login_required
def favourite_delete(request, id):
    movie = Movie.objects.get(id=id)
    favourite = ''
    data = {
        "movie": movie,
        "genres": movie.genres.all(),
        "persons": movie.actors.all(),
        'favourite': favourite
    }
    favourite = Favourite.objects.get(movie_id=id)
    favourite.delete()
    return render(request, 'movie/movie-favourite.html', context=data, )


@login_required
def favourite(request):
    movies_favourite = []
    userID = request.user.id
    favourites = Favourite.objects.filter(user_id=userID)
    for favourite in favourites:
        movies = Movie.objects.filter(id=favourite.movie_id)
        movies_favourite.append(movies)
    data = {
        'movies_favourite': movies_favourite
    }
    return render(request, 'movie/favourite-list.html', context=data, )


@login_required
def studio_view(request, id):
    data = {
        'studio': Studio.objects.get(id=id),
        "countries": Country.objects.all()
    }
    return render(request, 'studio/studio-view.html', context=data, )


@login_required
def studio_detail(request, id):
    studioReq = Studio.objects.get(id=id)
    studio = StudioForm(instance=studioReq)
    data = {
        'studioObject': studioReq,
        'form': studio,
        "countries": Country.objects.all()
    }
    return render(request, 'studio/studio-detail.html', context=data, )


@login_required
def studio_list(request):
    data = {
        'studios': Studio.objects.all()
    }
    return render(request, 'studio/studio-list.html', context=data, )


@login_required
def studio_delete(request, id):
    try:
        studio = Studio.objects.get(id=id)
        studio.delete()
        return HttpResponseRedirect('/cine/studio-list')
    except ObjectDoesNotExist:
        data = {
            'error': 'Estudio no encontrado'
        }
        return render(request, 'cine/error-404.html', context=data, )


@login_required
def studio_new(request):
    studio = StudioForm()
    data = {
        'form': studio,
        "countries": Country.objects.all()
    }
    return render(request, 'studio/studio-detail.html', context=data, )


@login_required
def studio_save(request):
    id_studio = request.POST.get('id')
    country_id_str = request.POST.get("country_id")
    country_id = int(country_id_str) if country_id_str else None
    if id_studio == '':
        form = StudioForm(request.POST, request.POST.get('logo_url'), request.FILES)
        if request.POST.get('logo_url') != '':
            url = request.POST.get('logo_url')
            url_web(url)
            form.instance.logo = myimage
            form = StudioForm(request.POST)
        else:
            form = StudioForm(request.POST, request.FILES)
    else:
        id_studio = int(id_studio)
        studio = Studio.objects.get(id=id_studio)
        studio.country_id = country_id
        form = StudioForm(request.POST, request.POST.get('logo_url'), request.FILES, instance=studio)
        if request.POST.get('logo_url') != '':
            url = request.POST.get('logo_url')
            url_web(url)
            studio.logo = myimage
            form = StudioForm(request.POST, instance=studio)
        else:
            form = StudioForm(request.POST, request.FILES, instance=studio)
            studio.logo = request.FILES.get('logo')
    if not form.is_valid():
        return HttpResponseRedirect('/cine/studio-new')
    location = 'static/img'
    path = os.path.join(location, str(request.FILES.get('logo')))
    if os.path.exists(path):
        os.remove(path)
    studio = form.save()
    return redirect('studio-view', id=studio.id)


@login_required
def country_view(request, id):
    data = {
        'country': Country.objects.get(id=id)
    }
    return render(request, 'country/country-view.html', context=data, )


@login_required
def country_detail(request, id):
    countryReq = Country.objects.get(id=id)
    country = CountryForm(instance=countryReq)
    data = {
        'countryObject': countryReq,
        'form': country
    }
    return render(request, 'country/country-detail.html', context=data, )


@login_required
def country_list(request):
    data = {
        'countries': Country.objects.all()
    }
    return render(request, 'country/country-list.html', context=data, )


@login_required
def country_delete(request, id):
    try:
        country = Country.objects.get(id=id)
        country.delete()
        return HttpResponseRedirect('/cine/country-list')
    except ObjectDoesNotExist:
        data = {
            'error': 'País no encontrado'
        }
        return render(request, 'cine/error-404.html', context=data, )


@login_required
def country_new(request):
    country = CountryForm()
    data = {
        'form': country
    }
    return render(request, 'country/country-detail.html', context=data, )


@login_required
def country_save(request):
    id_country = request.POST.get('id')
    if id_country == '':
        form = CountryForm(request.POST, request.POST.get('flag_url'), request.FILES)
        if request.POST.get('flag_url') != '':
            url = request.POST.get('flag_url')
            url_web(url)
            form.instance.national_flag = myimage
            form = CountryForm(request.POST)
        else:
            form = CountryForm(request.POST, request.FILES)
    else:
        id_country = int(id_country)
        country = Country.objects.get(id=id_country)
        form = CountryForm(request.POST, request.POST.get('flag_url'), request.FILES, instance=country)
        if request.POST.get('flag_url') != '':
            url = request.POST.get('flag_url')
            url_web(url)
            country.national_flag = myimage
            form = CountryForm(request.POST, instance=country)
        else:
            form = CountryForm(request.POST, request.FILES, instance=country)
            country.national_flag = request.FILES.get('national_flag')
    if not form.is_valid():
        return HttpResponseRedirect('/cine/country-new')
    location = 'static/img'
    path = os.path.join(location, str(request.FILES.get('national_flag')))
    if os.path.exists(path):
        os.remove(path)
    country = form.save()
    return redirect('country-view', id=country.id)


@login_required
def genre_view(request, id):
    data = {
        'genre': Genre.objects.get(id=id)
    }
    return render(request, 'genre/genre-view.html', context=data, )


@login_required
def genre_detail(request, id):
    genreReq = Genre.objects.get(id=id)
    genre = GenreForm(instance=genreReq)
    data = {
        'genreObject': genreReq,
        'form': genre
    }
    return render(request, 'genre/genre-detail.html', context=data, )


@login_required
def genre_list(request):
    data = {
        'genres': Genre.objects.all()
    }
    return render(request, 'genre/genre-list.html', context=data, )


@login_required
def genre_delete(request, id):
    try:
        genre = Genre.objects.get(id=id)
        genre.delete()
        return HttpResponseRedirect('/cine/genre-list')
    except ObjectDoesNotExist:
        data = {
            'error': 'Género no encontrado'
        }
        return render(request, 'cine/error-404.html', context=data, )


@login_required
def genre_new(request):
    genre = GenreForm()
    data = {
        'form': genre
    }
    return render(request, 'genre/genre-detail.html', context=data, )


@login_required
def genre_save(request):
    id_genre = request.POST.get('id')
    if id_genre == '':
        form = GenreForm(request.POST)
    else:
        id_genre = int(id_genre)
        genre = Genre.objects.get(id=id_genre)
        form = GenreForm(request.POST, instance=genre)
    if not form.is_valid():
        return HttpResponseRedirect('/cine/genre-new')
    genre = form.save()
    return redirect('genre-view', id=genre.id)


# Vistas de personas


@login_required
def actor(request):
    pagina = Paginator(Actor.objects.order_by('apellidos'), 4)
    suj = pagina.get_page(request.GET.get('page'))  # Si no hay resultados con request.GET.page, devuelve 1.
    rango = pagina.page_range
    data = {
        "personas": suj,
        "rango": rango,
        "positivo": len(rango)
    }
    return render(request, "actor/actor-list.html", context=data)


@login_required
def director(request):
    pagina = Paginator(Director.objects.order_by('apellidos'), 4)
    suj = pagina.get_page(request.GET.get('page'))  # Si no hay resultados con request.GET.page, devuelve 1.
    rango = pagina.page_range
    data = {
        "personas": suj,
        "rango": rango,
        "positivo": len(rango)
    }
    return render(request, "director/director-list.html", context=data)


@login_required
def filtro_actor(request, clave):
    actor = Actor.objects.get(id=clave)
    pelis = Movie.objects.order_by('date')
    vector = []
    for peli in pelis:
        if actor in peli.actors.all():
            vector.append(peli)
    data = {
        "persona": actor,
        "pelis": vector,
        "largo": len(vector)
    }
    return render(request, "actor/actor-view.html", context=data)


@login_required
def filtro_director(request, clave):
    peliculas = Movie.objects.filter(director=clave).order_by('date')
    data = {
        "persona": Director.objects.get(id=clave),
        "pelis": peliculas,
        "largo": len(peliculas)
    }
    return render(request, "director/director-view.html", context=data)


@login_required
def borra_actor(request, clave):
    persona = Actor.objects.get(id=clave)
    try:
        os.remove(persona.foto.path)
    except:  # Nunca debería ocurrir que un actor carezca de foto.
        print("Foto inexistente")
    finally:
        persona.biografia.delete()
        persona.delete()
        return HttpResponseRedirect("/cine/actor/")


@login_required
def borra_director(request, clave):
    director = Director.objects.get(id=clave)
    try:
        os.remove(director.foto.path)
    except:  # Nunca debería ocurrir que un actor carezca de foto.
        print("Foto inexistente")
    finally:
        director.biografia.delete()
        director.delete()
        return HttpResponseRedirect("/cine/director/")


@login_required
def guardar_actor(request):
    modificacion = request.POST.get("id")
    patria = Country.objects.get(id=int(request.POST.get("pais")))
    ruta = request.POST.get('image_url')
    if ruta != '':
        foto = ruta
    else:
        path = os.path.join('static/img', str(request.FILES.get("foto")))
        print(path)
        if os.path.exists(path):
            os.remove(path)
        foto = request.FILES.get("foto")
    fecha = request.POST.get("nacimiento")
    if fecha == "":
        fecha = date.today()
    if modificacion:
        codigo = int(modificacion)
        persona = Actor.objects.get(id=codigo)
        persona.nombre = request.POST.get("nombre")
        persona.apellidos = request.POST.get("apellidos")
        biografia = persona.biografia
        biografia.texto = request.POST.get("biografia")
        biografia.save()
        # Si modificas una persona, puedes dejar la variable de la foto en blanco para no sustituirla.
        if foto:
            if ruta != '':
                url_web(ruta)
                persona.foto = myimage
            else:
                persona.foto = foto
        persona.pais = patria
        persona.nacimiento = fecha
        persona.save()
    else:
        if ruta != '':
            url_web(ruta)
        biografia = Biografia.objects.create(texto=request.POST.get("biografia"))
        persona = Actor.objects.create(
            nombre=request.POST.get("nombre"),
            apellidos=request.POST.get("apellidos"),
            biografia=biografia,
            foto=foto,
            pais=patria,
            nacimiento=fecha
        )
    return HttpResponseRedirect("/cine/filtrar_actor/{}/".format(persona.id))


@login_required
def guardar_director(request):
    modificacion = request.POST.get("id")
    patria = Country.objects.get(id=int(request.POST.get("pais")))
    ruta = request.POST.get('image_url')
    if ruta != '':
        foto = ruta
    else:
        path = os.path.join('static/img', str(request.FILES.get("foto")))
        print(path)
        if os.path.exists(path):
            os.remove(path)
        foto = request.FILES.get("foto")
    fecha = request.POST.get("nacimiento")
    if fecha == "":
        fecha = date.today()
    if modificacion:
        codigo = int(modificacion)
        persona = Director.objects.get(id=codigo)
        persona.nombre = request.POST.get("nombre")
        persona.apellidos = request.POST.get("apellidos")
        biografia = persona.biografia
        biografia.texto = request.POST.get("biografia")
        biografia.save()
        # Si modificas una persona, puedes dejar la variable de la foto en blanco para no sustituirla.
        if foto:
            if ruta != '':
                url_web(ruta)
                persona.foto = myimage
            else:
                persona.foto = foto
        persona.pais = patria
        persona.nacimiento = fecha
        persona.save()
    else:
        if ruta != '':
            url_web(ruta)
        biografia = Biografia.objects.create(texto=request.POST.get("biografia"))
        persona = Director.objects.create(
            nombre=request.POST.get("nombre"),
            apellidos=request.POST.get("apellidos"),
            biografia=biografia,
            foto=foto,
            pais=patria,
            nacimiento=fecha
        )
    return HttpResponseRedirect("/cine/filtrar_director/{}/".format(persona.id))


@login_required
def crear_actor(request):
    data = {
        "paises": Country.objects.all(),
        "fecha": date.today()
    }
    return render(request, "actor/actor-new.html", context=data)


@login_required
def modifica_actor(request, clave):
    persona = Actor.objects.get(id=clave)
    data = {
        "persona": persona,
        "paises": Country.objects.all(),
        "fecha": persona.nacimiento
    }
    return render(request, "actor/actor-new.html", context=data)


@login_required
def crear_director(request):
    data = {
        "paises": Country.objects.all(),
        "fecha": date.today()
    }
    return render(request, "director/director-new.html", context=data)


@login_required
def modifica_director(request, clave):
    persona = Director.objects.get(id=clave)
    data = {
        "persona": persona,
        "paises": Country.objects.all(),
        "fecha": persona.nacimiento
    }
    return render(request, "director/director-new.html", context=data)


@login_required
def borra_director(request, clave):
    persona = Director.objects.get(id=clave)
    try:
        os.remove(persona.foto.path)
    except:  # Nunca debería ocurrir que un actor carezca de foto.
        print("Foto inexistente")
    finally:
        persona.biografia.delete()
        persona.delete()
        return HttpResponseRedirect("/cine/director/")


# VIEWS LUGARES
def crear_lugar(request):
    data = {
        "lugares": Lugar.objects.all(),
        "pais": Lugar.objects.all(),
        "ciudad": Lugar.objects.all(),
        "paraje": Lugar.objects.all(),
    }
    return render(request, "lugares/site-edit.html", context=data)


def filtro_lugar(request, clave):
    data = {
        "lugares": Lugar.objects.get(id=clave),
        "pais": Lugar.objects.all(),
        "ciudad": Lugar.objects.all(),
        "paraje": Lugar.objects.all(),
    }
    return render(request, "lugar/site-view.html", context=data)


@login_required
def site_list(request):
    data = {
        'lugares': Lugar.objects.all()
    }
    return render(request, 'lugares/site-list.html', context=data, )
