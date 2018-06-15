from django import forms
from core.models import *

class PartidaForm(forms.ModelForm):
    fkid_time = forms.ModelChoiceField(label="Time", queryset=Times.objects.all(), initial=0)
    qtd_gols = forms.IntegerField(label="Gols")
    
    
    class Meta:
        model = Partida
        exclude = ['pkid_partida', 'id_partida']