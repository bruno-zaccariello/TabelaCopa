# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import datetime

__all__ = ['Grupos', 'Partida', 'Times', 'Calendario']

class Grupos(models.Model):
    pkid_grupo = models.IntegerField(primary_key=True)
    nome_grupo = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.nome_grupo

    class Meta:
        managed = True
        db_table = 'grupos'
        verbose_name_plural = 'Grupos'


class Times(models.Model):
    pkid_time = models.IntegerField(primary_key=True)
    fkid_grupo = models.ForeignKey(Grupos, models.DO_NOTHING, db_column='fkid_grupo', blank=True, null=True)
    nome_time = models.CharField(unique=True, max_length=25, blank=True, null=True)
    vitorias = models.IntegerField(blank=True, null=True)
    empates = models.IntegerField(blank=True, null=True)
    derrotas = models.IntegerField(blank=True, null=True)
    pontos = models.IntegerField(blank=True, null=True)
    saldo_gols = models.IntegerField()

    def __str__(self):
        return self.nome_time

    class Meta:
        managed = True
        db_table = 'times'
        verbose_name_plural = 'Times'


class Partida(models.Model):
    pkid_partida = models.IntegerField(primary_key=True)
    fkid_time = models.ForeignKey('Times', models.DO_NOTHING, db_column='fkid_time')
    id_partida = models.CharField(max_length=2)
    qtd_gols = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'partida'
        
class Calendario(models.Model):
    pkid_calendario = models.IntegerField(primary_key=True)
    fkid_time = models.ForeignKey('Times', models.DO_NOTHING, db_column='fkid_time')
    id_partida = models.CharField(max_length=2)
    data = models.DateTimeField(default=datetime.datetime.now())
    
    class Meta:
        managed = True
        db_table = 'calendario'