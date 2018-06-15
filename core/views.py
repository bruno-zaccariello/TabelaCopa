from django.http import request, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.forms import formset_factory
from core.models import *
from core.forms import PartidaForm, CalendarioForm
import datetime
import operator

# Create your views here.

__all__ = ['index', 'add_partida', 'tab_grupo', 'add_calendario']

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
    lista = []
    for partida in Partida.objects.order_by('id_partida'):
        if len(lista) == 0 :
            lista.append(partida)
        elif partida.id_partida != lista[-1].id_partida:
            lista.append(partida)
    for partida in lista:
        if partida.id_partida[0] == grupo:
            if int(partida.id_partida[1]) == i:
                i += 1
            else:
                break
    id_partida =  grupo + str(i)
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
        calendario = Calendario.objects.filter(id_partida=id_partida)
        for item in calendario:
            item.finalizado = True
            item.save()
        time1.save()
        time2.save()
        PF1.save()
        PF2.save()
        return True
    except:
        print('deu ruim')

def add_partida(request):
    if request.POST:
        partidaForm = formset_factory(PartidaForm, extra=2, max_num=2)
        partidaForm = partidaForm(request.POST)
        if partidaForm.is_valid():
            update_db(partidaForm)
            return HttpResponseRedirect('/add_partida/8426')
    else:
        partidaForm = formset_factory(PartidaForm, extra=2, max_num=2)
    context = {
        'PartidaForm':partidaForm
    }
    return render(request, 'add_partida.html', context)

def make_id_calendario(calendarioform):
    grupo = str(calendarioform.fkid_time.fkid_grupo.nome_grupo.split(' ')[1])
    i = 1
    lista = []
    for partida in Calendario.objects.order_by('id_partida'):
        if len(lista) == 0 :
            lista.append(partida)
        elif partida.id_partida != lista[-1].id_partida:
            lista.append(partida)
    for partida in lista:
        if partida.id_partida[0] == grupo:
            if int(partida.id_partida[1]) == i:
                i += 1
            else:
                break
    id_partida =  grupo + str(i)
    print(id_partida)
    return id_partida

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
            return HttpResponseRedirect('/add_calendario/8426')
    else:
        calendarioForm = formset_factory(CalendarioForm, extra=2, max_num=2)
    context = {
        'CalendarioForm':calendarioForm
    }
    return render(request, 'add_calendario.html', context)

def tab_grupo(request, id_grupo):
    grupo = Grupos.objects.get(pkid_grupo=id_grupo)
    times = list(Times.objects.filter(fkid_grupo=grupo))
    times.sort(key=operator.attrgetter('pontos', 'saldo_gols', 'vitorias'), reverse=True)
    partidas = []
    for i in range(1,7):
        partidas.append( str(grupo.nome_grupo.split(' ')[1]) + str(i) )
    jogos = []
    for partida in partidas:
        jogos.append( (list(Calendario.objects.filter(id_partida=partida)),
                       list(Partida.objects.filter(id_partida=partida)) )
                    )
    print(jogos)
    context = {
        'grupo':grupo,
        'times':times,
        'jogos':jogos,
    }
    return render(request, 'pag_grupo.html', context)