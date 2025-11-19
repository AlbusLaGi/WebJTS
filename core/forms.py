from django import forms
from .models import Inscripcion, Cuori # Importar Cuori
import re

class CuoriForm(forms.ModelForm):
    # Campos del modelo Cuori
    nombre_completo = forms.CharField(label="Nombre Completo", max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Nombre Completo'}))
    cedula = forms.CharField(label="Cédula", max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Cédula'}))
    numero_contacto = forms.CharField(label="Número de Contacto 1", min_length=10, max_length=10, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Número de Contacto Principal'}))
    numero_contacto_2 = forms.CharField(label="Número de Contacto 2 (Opcional)", min_length=10, max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Contacto Adicional'}))
    email_contacto = forms.EmailField(label="Correo Electrónico", required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}))
    pais = forms.CharField(label="País", max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País'}))
    departamento = forms.CharField(label="Departamento/Estado/Región", max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Departamento/Estado/Región'}))
    ciudad = forms.CharField(label="Ciudad", max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}))

    class Meta:
        model = Cuori
        fields = ['nombre_completo', 'cedula', 'numero_contacto', 'numero_contacto_2', 'email_contacto', 'pais', 'departamento', 'ciudad']

    def clean_nombre_completo(self):
        nombre_completo = self.cleaned_data['nombre_completo']
        nombre_completo = re.sub(r'\s+', ' ', nombre_completo).strip()
        return nombre_completo.upper()

    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        cedula = re.sub(r'[^0-9]', '', cedula)
        return cedula.upper()

    def clean_numero_contacto(self):
        numero_contacto = self.cleaned_data['numero_contacto']
        numero_contacto = re.sub(r'[^0-9]', '', numero_contacto)
        return numero_contacto

    def clean_email_contacto(self):
        email_contacto = self.cleaned_data['email_contacto']
        return email_contacto.lower()

    def clean_pais(self):
        pais = self.cleaned_data['pais']
        return pais.upper()

    def clean_departamento(self):
        departamento = self.cleaned_data['departamento']
        return departamento.upper()

    def clean_ciudad(self):
        ciudad = self.cleaned_data['ciudad']
        return ciudad.upper()

class InscripcionPublicaForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(label="Acepto los términos y condiciones y la política de Habeas Data", required=True)

    class Meta:
        model = Inscripcion
        fields = ['terms_accepted'] # Solo el campo de términos y condiciones

    