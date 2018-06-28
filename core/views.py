from django.http import request, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.forms import formset_factory
from core.models import *
from core.forms import PartidaForm, CalendarioForm
from django.contrib.auth.forms import UserCreationForm
from core.functions import *
import datetime
import operator

# Create your views here.

__all__ = ['index', 'add_partida', 'tab_grupo', 'add_calendario', 'cadastro', 'authenticate', 'user_profile', 'authenticate']

def authenticate(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('home')
	return render(request, 'authenticate.html')


def user_profile(request):
	return render(request, 'user_profile.html')
	
@login_required(login_url="authenticate")
def index(request):
    grupos = Grupos.objects.all()
    times = teams_by_user(request)
    content = []
    for grupo in grupos:
        tmp_g = []
        for time in times:
            if time['fkid_grupo_id'] == grupo.pkid_grupo:
                tmp_g.append(time)
        content.append((grupo, tmp_g))
    for g, t in content:
        pass
        t.sort(key=operator.itemgetter('pontos', 'saldo_gols', 'vitorias'), reverse=True)
    context = {
        'grupos':grupos,
        'content':content
    }
    return render(request, 'index.html', context)

@login_required(login_url="")
def add_partida(request):
    if request.POST:
        partidaForm = formset_factory(PartidaForm, extra=2, max_num=2)
        partidaForm = partidaForm(request.POST)
        if partidaForm.is_valid():
            update_db(request, partidaForm)
            return HttpResponseRedirect('/add_partida/')
    else:
        partidaForm = formset_factory(PartidaForm, extra=2, max_num=2)
    context = {
        'PartidaForm':partidaForm
    }
    return render(request, 'add_partida.html', context)

@login_required(login_url="")
def add_calendario(request):
    if request.POST:
        calendarioForm = formset_factory(CalendarioForm, extra=2, max_num=2)
        calendarioForm = calendarioForm(request.POST)
        data = request.POST.get('data_input')
        if calendarioForm.is_valid():
            partidas = []
            for form in calendarioForm:
                partidas.append(form)
            PF1 = partidas[0].save(commit=False)
            PF2 = partidas[1].save(commit=False)
            id_partida = make_id_calendario(PF1)
            PF1.id_partida = id_partida
            PF2.id_partida = id_partida
            data = fix_data(data) 
            PF1.data = data
            PF2.data = data
            PF1.save()
            PF2.save()
            return HttpResponseRedirect('/add_calendario/')
    else:
        calendarioForm = formset_factory(CalendarioForm, extra=2, max_num=2)
    context = {
        'CalendarioForm':calendarioForm
    }
    return render(request, 'add_calendario.html', context)


def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/login/')
    else:
        form = UserCreationForm()
    context = {
        'form':form
    }
    return render(request, 'registrar_user.html', context)

def tab_grupo(request, id_grupo):
    grupo = Grupos.objects.get(pkid_grupo=id_grupo)
    times = list(teams_by_user(request, id_grupo))
    times.sort(key=operator.itemgetter('pontos', 'saldo_gols', 'vitorias'), reverse=True)
    partidas = []
    for i in range(1,7):
        partidas.append( str(grupo.nome_grupo.split(' ')[1]) + str(i) )
    jogos = []
    for partida in partidas:
        jogos.append( (list(Calendario.objects.filter(id_partida=partida)),
                       list(Partida.objects.filter(id_partida=partida, 
                                                   fkid_user = request.user.id))
                      )
                    )
    print(jogos)
    context = {
        'grupo':grupo,
        'times':times,
        'jogos':jogos,
    }
    return render(request, 'pag_grupo.html', context)