# -*- encoding: utf-8 -*-
__author__ = 'edison'
from django import forms
from .models import *

# ----------------------------------------------------------usuario----------------------------------------------------
class UserForm(forms.ModelForm):
    per_cedula=forms.CharField(label="Cedula",widget=forms.TextInput(attrs={
        'class':'validate','type':'text'}))
    per_nombre=forms.CharField(label="Nombres",widget=forms.TextInput(attrs={
        'class':'validate'}))
    per_apellido=forms.CharField(label="Apellidos",widget=forms.TextInput(attrs={
        'class':'validate'}))
    class Meta:
        model = User
        widgets={
            'carr_id':forms.Select(attrs={
                'class':'browser-default'
            }),
            'tip_id':forms.Select(attrs={
                'class':'browser-default'
            })
        }
        fields = ('per_cedula','per_nombre','per_apellido','carr_id','tip_id',)


class UserFormADM(forms.ModelForm):
    per_cedula=forms.CharField(label="Cedula",widget=forms.TextInput(attrs={
        'class':'validate','type':'text'}))
    per_nombre=forms.CharField(label="Nombres",widget=forms.TextInput(attrs={
        'class':'validate'}))
    per_apellido=forms.CharField(label="Apellidos",widget=forms.TextInput(attrs={
        'class':'validate'}))
    is_active=forms.BooleanField(label="Estado",widget=forms.CheckboxInput(attrs={
        'type':'checkbox'}))
    class Meta:
        model = User
        widgets={
            'carr_id':forms.Select(attrs={
                'class':'browser-default'
            }),
            'tip_id':forms.Select(attrs={
                'class':'browser-default'
            })
        }
        fields = ('per_cedula','per_nombre','per_apellido','carr_id','tip_id','is_active',)


class EditarContrasenaForm(forms.Form):

    actual_password = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={'class': 'validate'}))

    password = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'validate'}))

    password2 = forms.CharField(
        label='Repetir contraseña',
        widget=forms.PasswordInput(attrs={'class': 'validate'}))

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contrasenias no coinciden.')
        return password2


class ServiciosForm(forms.ModelForm):
    serv_nombre=forms.CharField(label="Nombre",widget=forms.TextInput(attrs={
        'class':'validate','type':'text'}))

    serv_descripcion=forms.CharField(label="Descripcion",widget=forms.Textarea(attrs={
        'class':'materialize-textarea'}))

    serv_estado=forms.BooleanField(label="Estado",widget=forms.CheckboxInput(attrs={
        'type':'checkbox'}))
    class Meta:
        model = Servicio
        fields = '__all__'


class ComputadorForm(forms.ModelForm):
    comp_id=forms.CharField(label="Direccion MAC",widget=forms.TextInput(attrs={
        'class':'validate','type':'text'}))
    comp_numero=forms.CharField(label="Numero de Computador",widget=forms.TextInput(attrs={
        'class':'validate'}))
    comp_marca=forms.CharField(label="Marca",widget=forms.TextInput(attrs={
        'class':'validate'}))
    comp_serie=forms.CharField(label="Numero de Serie",widget=forms.TextInput(attrs={
        'class':'validate'}))
    comp_so=forms.CharField(label="Sistema Operativo",widget=forms.TextInput(attrs={
        'class':'validate'}))
    comp_anio=forms.CharField(label="Año",widget=forms.TextInput(attrs={
        'class':'validate'}))
    comp_ram=forms.CharField(label="Capacidad de RAM",widget=forms.TextInput(attrs={
        'class':'validate'}))
    comp_disco_d=forms.CharField(label="Capacidad de Disco Duro",widget=forms.TextInput(attrs={
        'class':'validate'}))
    comp_procesador=forms.CharField(label="Capacidad de Procesador",widget=forms.TextInput(attrs={
        'class':'validate'}))
    comp_estado=forms.BooleanField(label="Estado",widget=forms.CheckboxInput(attrs={
        'type':'checkbox'}))
    class Meta:
        model = Computador
        fields = ('comp_id','comp_numero','comp_marca','comp_serie','comp_so','comp_anio','comp_ram','comp_disco_d','comp_procesador','comp_estado',)


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = SolicitudServicio
        fields = '__all__'


class U_A_Form(forms.ModelForm):
    ua_nombre=forms.CharField(label="Nombre",widget=forms.TextInput(attrs={
        'class':'validate','type':'text'}))
    ua_descripcion=forms.CharField(label="Descripcion",widget=forms.Textarea(attrs={
        'class':'materialize-textarea'}))
    dep_codigo=forms.CharField(label="Codigo de departamento",widget=forms.TextInput(attrs={
        'class':'validate'}))
    class Meta:
        model = Unidad_academica
        fields = '__all__'


class CarreraForm(forms.ModelForm):
    carr_nombre=forms.CharField(label="Nombre",widget=forms.TextInput(attrs={
        'class':'validate','type':'text'}))
    carr_descripcion=forms.CharField(label="Descripcion",widget=forms.Textarea(attrs={
        'class':'materialize-textarea'}))
    dep_codigo=forms.CharField(label="Codigo de departamento",widget=forms.TextInput(attrs={
        'class':'validate'}))
    class Meta:
        model = Carrera
        widgets={
            'ua_id':forms.Select(attrs={
                'class':'browser-default'
            })
        }
        fields = '__all__'


class TipoForm(forms.ModelForm):
    tip_nombre=forms.CharField(label="Nombre de tipo de persona",widget=forms.TextInput(attrs={
        'class':'validate','type':'text'}))
    class Meta:
        model = Tipo_persona
        fields = '__all__'

class ImporteForm(forms.ModelForm):
    imp_archvio=forms.FileField(label="Selccione un archivo csv",widget=forms.FileInput(attrs={
        'type':'file'}))
    class Meta:
        model = Importe
        widgets={
            'imp_carrera':forms.Select(attrs={
                'class':'browser-default'
            })
        }
        fields = '__all__'
