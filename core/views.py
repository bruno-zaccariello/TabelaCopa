from django.http import request, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.forms import formset_factory
from core.models import *
from core.forms import PartidaForm
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
        t.sort(key=operator.attrgetter('pontos', 'saldo_gols', 'vitorias'), reverse=True)
    context = {
        'grupos':grupos,
        'content':content
    }
    return render(request, 'grupos.html', context)

def make_id(partidaform):
    grupo = str(partidaform.fkid_time.fkid_grupo.nome_grupo.split(' ')[1])
    i = 1
    for partida in Partida.objects.all():
        if partida.id_partida[0] == grupo:
            if partida.id_partida[1] == i:
                i += 1
            else:
                i += 1
                break
    id_partida =  grupo + str(i)
    print('ok id_partida')
    print(id_partida)
    return id_partida

def update_db(PartidaForm):
    try:
        partidas = []
        for form in PartidaForm:
            partidas.append(form)
        PF1 = partidas[0].save(commit=False)
        PF2 = partidas[1].save(commit=False)
        time1 = PF1.fkid_time
        time2 = PF2.fkid_time
        if PF1.qtd_gols > PF2.qtd_gols:
            time1.vitorias += 1
            time1.saldo_gols += (PF1.qtd_gols - PF2.qtd_gols) 
            time1.pontos += 3
            time2.derrotas += 1
            time2.saldo_gols += (PF2.qtd_gols - PF1.qtd_gols) 
            time2.pontos += 0
        elif PF2.qtd_gols > PF1.qtd_gols:
            time2.vitorias += 1
            time2.saldo_gols += (PF2.qtd_gols - PF1.qtd_gols) 
            time2.pontos += 3
            time1.derrotas += 1
            time1.saldo_gols += (PF1.qtd_gols - PF2.qtd_gols) 
            time1.pontos += 0
        else:
            time1.empates += 1
            time1.pontos += 1
            time2.empates += 1
            time2.pontos += 1
        id_partida = make_id(PF1)
        PF1.id_partida = id_partida
        PF2.id_partida = id_partida
        time1.save()
        time2.save()
        PF1.save()
        PF2.save()
        print('ok update_db')
        return True
    except:
        print('deu ruim')

def add_partida(request):
    if request.POST:
        partidaForm = formset_factory(PartidaForm, extra=2, max_num=2)
        partidaForm = partidaForm(request.POST)
        if partidaForm.is_valid():
            update_db(partidaForm)
            print('ok tudo')
            return HttpResponseRedirect('/add_partida')
    else:
        partidaForm = formset_factory(PartidaForm, extra=2, max_num=2)
    context = {
        'PartidaForm':partidaForm
    }
    return render(request, 'add_partida.html', context)

def tab_grupo(request, id_grupo):
    grupo = Grupos.objects.get(pkid_grupo=id_grupo)
    times = list(Times.objects.filter(fkid_grupo=grupo))
    times.sort(key=operator.attrgetter('pontos', 'saldo_gols', 'vitorias'), reverse=True)
    context = {
        'grupo':grupo,
        'times':times,
    }
    return render(request, 'pag_grupo.html', context)