# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

__all__ = ['Grupos', 'Partida', 'Times', 'Calendario', 'TimesInfo', 'AuthUser']


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    last_name = models.CharField(max_length=150)

    class Meta:
        managed = True
        db_table = 'auth_user'


class Calendario(models.Model):
    pkid_calendario = models.AutoField(primary_key=True)
    id_partida = models.CharField(max_length=2)
    fkid_time = models.ForeignKey('Times', models.DO_NOTHING, db_column='fkid_time')
    data = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'DT_{self.id_partida}'
    
    class Meta:
        managed = True
        db_table = 'calendario'


class Grupos(models.Model):
    pkid_grupo = models.AutoField(primary_key=True)
    nome_grupo = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.nome_grupo
    
    class Meta:
        managed = True
        db_table = 'grupos'


class Partida(models.Model):
    pkid_partida = models.AutoField(primary_key=True)
    fkid_time = models.ForeignKey('Times', models.DO_NOTHING, db_column='fkid_time')
    id_partida = models.CharField(max_length=2)
    qtd_gols = models.IntegerField()
    fkid_user = models.IntegerField()

    def __str__(self):
        return f'PD_{self.id_partida}'
    
    class Meta:
        managed = True
        db_table = 'partida'


class TimesInfo(models.Model):
    pkid_info_time = models.AutoField(primary_key=True)
    fkid_time = models.ForeignKey('Times', models.DO_NOTHING, db_column='fkid_time')
    fkid_user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='fkid_user')
    vitorias = models.IntegerField(blank=True, null=True)
    empates = models.IntegerField(blank=True, null=True)
    derrotas = models.IntegerField(blank=True, null=True)
    pontos = models.IntegerField(blank=True, null=True)
    saldo_gols = models.IntegerField()

    def update(self, info):
        if info.get('vitorias'):
            self.vitorias += info['vitorias']
        if info.get('empates'):
            self.empates += info['empates']
        if info.get('derrotas'):
            self.derrotas += info['derrotas']
        if info.get('pontos'):
            self.pontos += info['pontos']
        if info.get('saldo_gols'):
            self.saldo_gols += info['saldo_gols']
        self.save()
        return self
    
    def __str__(self):
        return f'{self.fkid_user}_{self.fkid_time}'
    
    class Meta:
        managed = True
        db_table = 'info_time'


class Times(models.Model):
    pkid_time = models.AutoField(primary_key=True)
    fkid_grupo = models.ForeignKey(Grupos, models.DO_NOTHING, db_column='fkid_grupo', blank=True, null=True)
    nome_time = models.CharField(unique=True, max_length=25, blank=True, null=True)

    def __str__(self):
        return self.nome_time
    
    class Meta:
        managed = True
        db_table = 'times'
