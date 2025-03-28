from django.db import models
import os
from datetime import datetime
from django.core.validators import FileExtensionValidator, MaxValueValidator

def media_upload_path(instance, filename):
    # Organise les fichiers dans des dossiers par type et par date
    date_part = instance.uploaded_at.date() if instance.uploaded_at else datetime.now().date()
    return f"{instance.media_type}s/{date_part}/{filename}"

class MediaFile(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    file = models.FileField(
        upload_to=media_upload_path,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi']),
        ]
    )
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.PositiveIntegerField(help_text="Taille du fichier en octets")
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def save(self, *args, **kwargs):
        # Vérifier la taille du fichier
        if self.file.size > 25 * 1024 * 1024:  # 25 Mo
            raise ValueError("La taille du fichier ne doit pas dépasser 25 Mo")
        
        # Définir le type de média
        self.media_type = 'image' if self.file.name.lower().split('.')[-1] in ['jpg', 'jpeg', 'png', 'gif'] else 'video'
        
        # Définir la taille
        self.size = self.file.size
        
        # Si uploaded_at n'est pas défini, utilisez le temps actuel
        if not self.uploaded_at:
            self.uploaded_at = datetime.now()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.media_type} - {self.file.name}"