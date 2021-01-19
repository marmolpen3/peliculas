import shelve

from django.shortcuts import render
from recomendador.populate import populateDatabase
from .models import Puntuacion, Pelicula
from .forms import FormularioUsuario
from .recommendations import getRecommendations, getRecommendedItems, calculateSimilarItems

# Create your views here.
# Prefs = {'usuarioId0': {'peliculaId0':puntuacion, 'peliculaId1':puntuacion},
#           'usuarioId1': {'peliculaId0':puntuacion, 'peliculaId1':puntuacion}}

def loadDict():
    UserPrefs = {}
    PeliPrefs = {}
    shelf = shelve.open("dataRS.dat")
    puntuaciones = Puntuacion.objects.all()
    for puntuacion in puntuaciones:
        usuario_id = int(puntuacion.usuario.id)
        pelicula_id = int(puntuacion.pelicula.id)
        rating = float(puntuacion.rating)

        UserPrefs.setdefault(usuario_id, {})
        UserPrefs[usuario_id][pelicula_id] = rating

        PeliPrefs.setdefault(pelicula_id, {})
        PeliPrefs[pelicula_id][usuario_id] = rating

    shelf['UsuariosPreferencias'] = UserPrefs
    shelf['PeliculaPreferencias'] = PeliPrefs
    shelf.close()

def index(request):
    template_name = "index.html"
    return render(request, template_name)

def populateDB(request):
    populateDatabase()
    return render(request,'populate.html')

def populateDict(request):
    loadDict()
    return render(request, 'populate.html')

def recomendador_por_usuario(request):
    if request.method == 'GET':
        form = FormularioUsuario(request.GET)
        if form.is_valid():
            usuario_id = form.cleaned_data['usuario_id']
            shelf = shelve.open("dataRS.dat")
            usuarios_prefs = shelf['UsuariosPreferencias']
            shelf.close()
            rankings = getRecommendations(usuarios_prefs, usuario_id)
            recommended = rankings[:2]
            recomendaciones = []
            for re in recommended:
                puntuacion = int(re[0])
                pelicula = Pelicula.objects.get(id=int(re[1]))
                recomendaciones.append((pelicula, puntuacion))

            return render(request, 'recomendaciones_usuario.html', {'recomendaciones':recomendaciones})

    form = FormularioUsuario()
    return render(request, 'formulario_usuario.html', {'form':form})

def recomendador_por_pelicula(request):
    if request.method == 'GET':
        form=FormularioUsuario(request.GET)
        if form.is_valid():
            usuario_id = form.cleaned_data['usuario_id']
            shelf = shelve.open("dataRS.dat")
            usuarios_prefs = shelf['UsuariosPreferencias']
            pelicula_prefs = shelf['PeliculaPreferencias']
            shelf.close()
            coincidencias_entre_peliculas=calculateSimilarItems(pelicula_prefs)
            rankings=getRecommendedItems(usuarios_prefs, coincidencias_entre_peliculas, usuario_id)
            recomendadas = rankings[:2]
            recomendaciones = []
            for re in recomendadas:
                puntuacion = int(re[0])
                pelicula = Pelicula.objects.get(id=int(re[1]))
                recomendaciones.append((pelicula, puntuacion))

            return render(request, 'recomendaciones_usuario.html', {'recomendaciones':recomendaciones})

    form=FormularioUsuario()
    return render(request, 'formulario_usuario_pelicula.html', {'form':form})