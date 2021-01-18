from django.shortcuts import render
from recomendador.populate import populateDatabase

# Create your views here.

def index(request):
    template_name = "index.html"
    return render(request, template_name)

def populateDB(request):
    populateDatabase()
    return render(request,'populate.html')

