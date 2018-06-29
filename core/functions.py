from core.models import *
from django.db import transaction

__all__ = ['make_id', 'update_db', 'make_id_calendario', 'teams_by_user']


def teams_by_user(request, grupo=None):
    times = Times.objects.all().values()
    if grupo:
        times = Times.objects.filter(fkid_grupo=grupo).values()
        print(times)
    for time in times:
        try:
            info = TimesInfo.objects.get(fkid_time=time['pkid_time'], fkid_user=request.user.id)
            info = {
                'vitorias':info.vitorias,
                'empates':info.empates,
                'derrotas':info.derrotas,
                'pontos':info.pontos,
                'saldo_gols':info.saldo_gols,
            }
            time.update(info)
        except:
            info = {
                'vitorias':0,
                'empates':0,
                'derrotas':0,
                'pontos':0,
                'saldo_gols':0,
            }
            time.update(info)
    return times

def make_id(partidaform):
    grupo = str(partidaform.fkid_time.fkid_grupo.nome_grupo.split(' ')[1])
    i = 1
    lista = []
    for partida in Partida.objects.filter(fkid_user=user.id).order_by('id_partida'):
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

def calculate_points(PF1, PF2):     
    if PF1.qtd_gols > PF2.qtd_gols:
        response = {
            't1':{
                'vitorias':1,
                'saldo_gols':(PF1.qtd_gols - PF2.qtd_gols),
                'pontos':3
            },
            't2':{
                'derrotas':1,
                'saldo_gols':(PF2.qtd_gols - PF1.qtd_gols),
            }
        }
    elif PF2.qtd_gols > PF1.qtd_gols:
        response = {
            't2':{
                'vitorias':1,
                'saldo_gols':(PF2.qtd_gols - PF1.qtd_gols),
                'pontos':3
            },
            't1':{
                'derrotas':1,
                'saldo_gols':(PF1.qtd_gols - PF2.qtd_gols),
            }
        }
    else:
        response = {
            't1':{
                'empates':1,
                'pontos':1
            },
            't2':{
                'empates':1,
                'pontos':1
            }
        }
    return response
    
def update_db(request, PartidaForm):
    try:
        with transaction.atomic():
            user = AuthUser.objects.get(id=request.user.id)
            partidas = []
            for form in PartidaForm:
                partidas.append(form)

            # Get Instances
            PF1 = partidas[0].save(commit=False)
            PF2 = partidas[1].save(commit=False)   

            # Get or Create Teams from Instances
            time1, created = TimesInfo.objects.get_or_create(
                fkid_time=PF1.fkid_time,
                fkid_user=request.user.id,
                defaults={
                    'fkid_user': user,
                    'vitorias': 0,
                    'empates': 0,
                    'derrotas': 0,
                    'pontos': 0,
                    'saldo_gols': 0
                    }
                )

            time2, created = TimesInfo.objects.get_or_create(
                fkid_time=PF2.fkid_time,
                fkid_user=request.user.id,
                defaults={
                    'fkid_user': user,
                    'vitorias': 0,
                    'empates': 0,
                    'derrotas': 0,
                    'pontos': 0,
                    'saldo_gols': 0
                    }
                )

            # Update teams info
            info = calculate_points(PF1, PF2)
            print(vars(time1))
            print(vars(time2))
            time1.update(info.get('t1'))
            time2.update(info.get('t2'))

            # Make match ID, relate the FKs and save the matches
            id_partida = make_id(PF1)
            PF1.id_partida, PF2.id_partida = id_partida, id_partida
            PF1.fkid_user, PF2.fkid_user = request.user.id, request.user.id
            PF1.save()
            PF2.save()
            return True
    except:
        raise 'An error has occurred. Please contact admin'
		
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
