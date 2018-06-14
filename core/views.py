from django.shortcuts import render
from core.models import *
import operator

# Create your views here.

__all__ = ['index', 'add_partida', 'tab_grupo']

def index(request):
    grupos = Grupos.objects.all()
    times = Times.objects.all()
    content = []
    for grupo in grupos:
        tmp_g = []
        for time in times:
            if time.fkid_grupo == grupo:
                tmp_g.append(time)
        content.append((grupo, tmp_g))
    for g, t in content:
        t.sort(key=operator.attrgetter('vitorias', 'empates'))
    context = {
        'grupos':grupos,
        'content':content
    }
    return render(request, 'grupos.html', context)

def add_partida(request):
    return False

def tab_grupo(request, id_grupo):
    return False