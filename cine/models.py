from django.db import models


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'genres'

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    capital = models.CharField(max_length=50, blank=True, null=True)
    continent = models.CharField(max_length=50, blank=True, null=True)
    national_flag = models.FileField(upload_to='', blank=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'countries'

    def __str__(self):
        return self.name


class Studio(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    president = models.CharField(max_length=50, blank=True, null=True)
    foundation = models.IntegerField(default=1900, blank=True, null=True)
    logo = models.FileField(upload_to='', blank=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'studios'

    def __str__(self):
        return self.name + ' - ' + self.country


class Biografia(models.Model):
    texto = models.TextField(blank=False, null=False)

    objects = models.Manager()

    class Meta:
        db_table = 'biografia'
        ordering = ['texto']

    def __str__(self):
        return self.texto


class Actor(models.Model):
    nombre = models.CharField(max_length=10)
    apellidos = models.CharField(max_length=25)
    foto = models.FileField(upload_to='', unique=True)
    pais = models.ForeignKey(Country, on_delete=models.CASCADE)
    nacimiento = models.DateField()
    biografia = models.OneToOneField(Biografia, on_delete=models.CASCADE, null=False)

    objects = models.Manager()

    class Meta:
        db_table = 'actor'
        ordering = ['apellidos']

    def __str__(self):
        return self.nombre + " " + self.apellidos


class Director(models.Model):
    nombre = models.CharField(max_length=10)
    apellidos = models.CharField(max_length=25)
    foto = models.FileField(upload_to='', unique=True)
    pais = models.ForeignKey(Country, on_delete=models.CASCADE)
    nacimiento = models.DateField()
    biografia = models.OneToOneField(Biografia, on_delete=models.CASCADE, null=False)

    objects = models.Manager()

    class Meta:
        db_table = 'director'
        ordering = ['apellidos']

    def __str__(self):
        return self.nombre + " " + self.apellidos


class Movie(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='', blank=True, null=True)
    cost = models.IntegerField(default=0, blank=True, null=True)
    income = models.IntegerField(default=0, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True, blank=True)
    actors = models.ManyToManyField(Actor)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True,
                                blank=True)  # Many to one (muchas películas asociadas a un país
    genres = models.ManyToManyField(Genre)
    studio = models.ForeignKey(Studio, on_delete=models.SET_NULL, null=True,
                               blank=True)  # Many to one (muchas películas asociadas a un estudio

    objects = models.Manager()

    class Meta:
        db_table = 'movies'

    def __str__(self):
        return self.name


class Lugar(models.Model):
    pais = models.TextField(blank=True, null=True)
    ciudad = models.TextField(blank=True, null=True)
    paraje = models.TextField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'lugares'

    def __str__(self):
        return f"Lugares(pais = {self.pais}, " \
               f"ciudad= {self.ciudad}, " \
               f"paraje= {self.paraje})"

    def __repr__(self):
        return self.__str__()


class Favourite(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    movie_id = models.IntegerField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'favourites'

    def __str__(self):
        return str(self.user_id) + " " + str(self.movie_id)
