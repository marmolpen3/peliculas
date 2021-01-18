from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,URLValidator


# Create your models here.


class Ocupacion(models.Model):
    nombre = models.CharField(max_length=20)

class Genero(models.Model):
    tipo = models.CharField(max_length=30)
    numero = models.IntegerField(default=0)

class Usuario(models.Model):
    edad = models.IntegerField()
    sexo = models.CharField(max_length=1)
    ocupacion = models.ForeignKey(Ocupacion, on_delete=models.DO_NOTHING)
    codigo_postal = models.CharField(max_length=5)

class Pelicula(models.Model):
    nombre = models.CharField(max_length=80)
    fecha_estreno = models.DateField(null=True)
    fecha_estreno_video = models.DateField(null=True)
    imdb_url = models.URLField(validators=[URLValidator()])
    categorias = models.ManyToManyField(Genero)

class Puntuacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    fecha_puntuacion = models.DateField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
