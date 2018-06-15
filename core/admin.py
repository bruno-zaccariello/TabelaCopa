from django.contrib import admin
from django import forms
from core.models import *

# Register your models here.

class TimeForm(forms.ModelForm):

    def save(self, commit=True):
        time = super(TimeForm, self).save(commit=False)
        if commit:
            time.save()
        return time

    class Meta:
        model = Times
        exclude = ['pkid_time']

class GrupoForm(forms.ModelForm):

    def save(self, commit=True):
        grupo = super(GrupoForm, self).save(commit=False)
        if commit:
            grupo.save()
        return grupo

    class Meta:
        model = Grupos
        exclude = ['pkid_grupo']

class TimeAdmin(admin.ModelAdmin):
    form = TimeForm
    
class GrupoAdmin(admin.ModelAdmin):
    form = GrupoForm
        
admin.site.register(Times, TimeAdmin)
admin.site.register(Grupos, GrupoAdmin)
admin.site.register(Partida)