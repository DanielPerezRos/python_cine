from django.contrib import admin

# Register your models here.
from .models import Studio, Genre, Country, Movie, Actor, Lugar, Biografia, Director, Favourite

admin.site.register(Studio)
admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Lugar)
admin.site.register(Biografia)
admin.site.register(Favourite)
