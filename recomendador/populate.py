#encoding:utf-8

import datetime

from recomendador.models import Ocupacion, Genero, Usuario, Pelicula, Puntuacion

def deleteTables():
    Genero.objects.all().delete()
    Ocupacion.objects.all().delete()
    Usuario.objects.all().delete()
    Pelicula.objects.all().delete()

def cargar_occupation():

    lista=[]
    fileobj = open('./datos/u.occupation', "r", encoding="ISO-8859-1")

    for line in fileobj.readlines():
        lista.append(Ocupacion(nombre=str(line.strip())))
    fileobj.close()
    Ocupacion.objects.bulk_create(lista)

    print("Occupations inserted: " + str(Ocupacion.objects.count()))
    print("---------------------------------------------------------")


def cargar_genre():

    lista=[]
    fileobj = open('./datos/u.genre', "r", encoding="ISO-8859-1")

    for line in fileobj.readlines():
        linea = line.split('|')
        if len(linea) != 2:
            continue
        lista.append(Genero(tipo=linea[0].strip() , numero=int(linea[1].strip())))
    fileobj.close()
    Genero.objects.bulk_create(lista)

    print("Genres inserted: " + str(Genero.objects.count()))
    print("---------------------------------------------------------")

def cargar_user():
    lista=[]
    usuarios = {}
    fileobj = open('./datos/u.user', "r", encoding="ISO-8859-1")

    for line in fileobj.readlines():
        linea = line.split('|')
        if len(linea) != 5:
            continue
        u = Usuario(pk=int(linea[0].strip()), edad=int(linea[1].strip()), sexo=linea[2].strip(), ocupacion=Ocupacion.objects.get(nombre=linea[3].strip()), codigo_postal=linea[4].strip())
        lista.append(u)
        usuarios[int(linea[0].strip())] = u
    fileobj.close()
    Usuario.objects.bulk_create(lista)

    print("Users inserted: " + str(Usuario.objects.count()))
    print("---------------------------------------------------------")

    return usuarios

def cargar_peliculas():
    lista=[]
    categorias = {}
    peliculas = {}
    fileobj = open('./datos/u.item', "r", encoding="ISO-8859-1")

    for line in fileobj.readlines():
        linea = line.split('|')
        generos = linea[5:24]
        if len(linea) != 24:
            continue
        lista.append(Pelicula(
            pk=int(linea[0].strip()),
            nombre=linea[1].strip(),
            fecha_estreno=date_format(linea[2].strip()),
            fecha_estreno_video=date_format(linea[3].strip()),
            imdb_url=linea[4].strip()))

        categorias[int(linea[0].strip())]=get_generos(generos)

    fileobj.close()
    Pelicula.objects.bulk_create(lista)

    print("Films inserted: " + str(Pelicula.objects.count()))
    print("---------------------------------------------------------")

    for pelicula in Pelicula.objects.all():
        pelicula.categorias.set(categorias[pelicula.id])
        peliculas[pelicula.id]=pelicula

    return peliculas

def date_format(str_date):
    if not str_date:
        return None
    else:
        fecha = str_date.split("-")
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        day = int(fecha[0])
        month = months.index(fecha[1]) + 1
        year = int(fecha[2])

        return datetime.date(year,month,day)

def get_generos(lista_generos):
    generos = []
    i=0
    for g in lista_generos:
        if int(g) == 1:
            genero = Genero.objects.get(numero=i)
            generos.append(genero)
        i+=1
    return generos

def cargar_puntuaciones(u, p):
    lista=[]
    fileobj = open('./datos/u.data', "r", encoding="ISO-8859-1")

    for line in fileobj.readlines():
        linea = line.split()
        if len(linea) != 4:
            continue
        lista.append(Puntuacion(
            usuario=u[int(linea[0].strip())],
            pelicula=p[int(linea[1].strip())],
            rating=int(linea[2].strip()),
            fecha_puntuacion=datetime.datetime.fromtimestamp(int(linea[3].strip()))))

    fileobj.close()
    Puntuacion.objects.bulk_create(lista)

    print("Ratings inserted: " + str(Puntuacion.objects.count()))
    print("---------------------------------------------------------")

def populateDatabase():
    deleteTables()
    cargar_occupation()
    cargar_genre()
    u=cargar_user()
    p=cargar_peliculas()
    cargar_puntuaciones(u, p)
    print("Finished database population")