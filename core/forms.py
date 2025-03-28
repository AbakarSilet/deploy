from django import forms
from .models import MediaFile
from django.core.validators import FileExtensionValidator

class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['file']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Vérification de l'extension
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi']
            ext = file.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError("Type de fichier non supporté.")
            
            # Vérification de la taille
            if file.size > 25 * 1024 * 1024:  # 25 Mo
                raise forms.ValidationError("La taille du fichier ne doit pas dépasser 25 Mo.")
        return file