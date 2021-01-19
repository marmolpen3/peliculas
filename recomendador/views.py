import shelve

from django.shortcuts import render
from recomendador.populate import populateDatabase
from .models import Puntuacion, Pelicula
from .forms import UserForm, MostSimilarFilmsForm
from .recommendations import getRecommendations, topMatches

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

def recomendador_by_user(request):
    if request.method == 'GET':
        form = UserForm(request.GET)
        if form.is_valid():
            user_id = form.cleaned_data['id']
            shelf = shelve.open("dataRS.dat")
            user_prefs = shelf['UsuariosPreferencias']
            shelf.close()
            rankings = getRecommendations(user_prefs, user_id)
            recommended = rankings[:2]
            recomendaciones = []
            for re in recommended:
                pelicula = Pelicula.objects.get(id=int(re[1]))
                puntuacion = int(re[0])
                recomendaciones.append((pelicula, puntuacion))

            return render(request, 'user_recomendaciones.html', {'recomendaciones':recomendaciones})

    form = UserForm()
    return render(request, 'user_form.html', {'form':form})

def top_3_peliculas_similares(request):
    if request.method == 'GET':
        form = MostSimilarFilmsForm(request.GET)
        if form.is_valid():
            pelicula_id = form.cleaned_data['id']
            shelf = shelve.open("dataRS.dat")
            pelicula_prefs = shelf['PeliculaPreferencias']
            shelf.close()
            scores = topMatches(pelicula_prefs, pelicula_id, n=3)
            recomendaciones = []
            for s in scores:
                puntuacion = int(s[0])
                pelicula = Pelicula.objects.get(id=int(s[1]))
                recomendaciones.append((pelicula, puntuacion))

            return render(request, 'user_recomendaciones.html', {'recomendaciones':recomendaciones})

    form = MostSimilarFilmsForm()
    return render(request, 'formulario_pelicula.html', {'form':form})