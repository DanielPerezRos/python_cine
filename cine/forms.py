from django import forms

from .models import Genre, Studio, Country


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'value': '', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': '', 'class': 'form-control'})
        }
        labels = {
            'name': 'Nombre:',
            'description': 'Descripción:'
        }


class StudioForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all().order_by('name'))

    class Meta:
        model = Studio
        fields = ['name', 'country', 'president', 'foundation', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'value': '', 'class': 'form-control'}),
            'country': forms.Select(attrs={'value': '', 'class': 'form-control'}),
            'president': forms.TextInput(attrs={'value': '', 'class': 'form-control'}),
            'foundation': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'upload_to': '', 'class': 'form-control'}),
            'logo_url': forms.URLInput(attrs={'value': '', 'class': 'form-control'})
        }
        labels = {
            'name': 'Nombre:',
            'country': 'País:',
            'president': 'Presidente:',
            'foundation': 'Año fundación:',
            'logo': 'Logo:',
            'logo_url': 'Logo url:'
        }


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name', 'capital', 'continent', 'national_flag']
        widgets = {
            'name': forms.TextInput(attrs={'value': '', 'class': 'form-control'}),
            'capital' : forms.TextInput(attrs={'value': '', 'class': 'form-control'}),
            'continent': forms.TextInput(attrs={'value': '', 'class': 'form-control'}),
            'national_flag': forms.FileInput(attrs={'upload_to': '', 'class': 'form-control'}),
            'flag_url': forms.URLInput(attrs={'value': '', 'class': 'form-control'})
        }
        labels = {
            'name': 'Nombre:',
            'capital': 'Capital:',
            'continent': 'Continente:',
            'national_flag': 'Bandera:',
            'flag_url': 'Bandera url:'
        }


class ImgUrlForm(forms.ModelForm):
    class Meta:
        fields = ['image_url']
        widgets = {
            'image_url': forms.URLInput(attrs={'value': '', 'class': 'form-control'}),
        }
        labels = {
            'image_url': 'Imagen url:'
        }
