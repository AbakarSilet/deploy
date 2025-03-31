from django.db import models
from datetime import datetime

def media_upload_path(instance, filename):
    """Organise les fichiers dans des dossiers par type (images/videos) et par date"""
    return f"{instance.media_type}s/{datetime.now().date()}/{filename}"

class MediaFile(models.Model):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    
    file = models.FileField(
        upload_to=media_upload_path,
        validators=[
            models.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi']),
        ]
    )
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.PositiveIntegerField(editable=False)

    class Meta:
        ordering = ['-uploaded_at']
    
    def save(self, *args, **kwargs):
        # Taille maximale : 25 Mo
        if self.file.size > 25 * 1024 * 1024:
            raise ValueError("Fichier trop volumineux (max 25 Mo)")
        
        # Détermine automatiquement le type
        extension = self.file.name.lower().split('.')[-1]
        self.media_type = 'image' if extension in ['jpg', 'jpeg', 'png', 'gif'] else 'video'
        
        # Enregistre la taille
        self.size = self.file.size
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_media_type_display()} - {self.file.name}"