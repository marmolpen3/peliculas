import datetime

from recomendador.models import Ocupacion, Genero, Usuario, Pelicula

def deleteTables():
    Genero.objects.all().delete()
    Ocupacion.objects.all().delete()
    Usuario.objects.all().delete()

def cargar_occupation():

    lista=[]
    fileobj = open('./datos/u.occupation', "r")

    for line in fileobj.readlines():
        lista.append(Ocupacion(nombre=str(line.strip())))
    fileobj.close()
    Ocupacion.objects.bulk_create(lista)

    print("Occupations inserted: " + str(Ocupacion.objects.count()))
    print("---------------------------------------------------------")


def cargar_genre():

    lista=[]
    fileobj = open('./datos/u.genre', "r")

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
    fileobj = open('./datos/u.user', "r")

    for line in fileobj.readlines():
        linea = line.split('|')
        if len(linea) != 5:
            continue
        lista.append(Usuario(pk=int(linea[0]), edad=int(linea[1]), sexo=linea[2], ocupacion=Ocupacion.objects.get(nombre=linea[3]), codigo_postal=linea[4]))
    fileobj.close()
    Usuario.objects.bulk_create(lista)

    print("Users inserted: " + str(Usuario.objects.count()))
    print("---------------------------------------------------------")

def cargar_peliculas():
    lista=[]
    categorias = {}
    fileobj = open('./datos/u.item', "r")

    for line in fileobj.readlines():
        linea = line.split('|')
        generos = linea[5:24]
        if len(linea) != 24:
            continue
        lista.append(Pelicula(
            pk=int(linea[0]),
            nombre=linea[1],
            fecha_estreno=date_format(linea[2]),
            fecha_estreno_video=date_format(linea[3]),
            imdb_url=linea[4]))

        categorias[int(linea[0])]=get_generos(generos)

    fileobj.close()
    Pelicula.objects.bulk_create(lista)

    print("Films inserted: " + str(Pelicula.objects.count()))
    print("---------------------------------------------------------")

    for pelicula in Pelicula.objects.all():
        pelicula.categorias.set(categorias[pelicula.id])

def date_format(str_date):
    if not str_date:
        return None
    else:
        fecha = str_date.split("-")
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        day = int(fecha[0])
        print(type(months.index(fecha[1])))
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

def cargar_puntuaciones():
    #TODO

def populateDatabase():
    deleteTables()
    cargar_occupation()
    cargar_genre()
    cargar_user()
    cargar_peliculas()
    cargar_puntuaciones()
    print("Finished database population")