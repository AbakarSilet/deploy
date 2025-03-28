from django.contrib import admin
from .models import MediaFile
from django.utils.safestring import mark_safe
from django.urls import reverse

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('preview', 'name', 'media_type', 'formatted_size', 'uploaded_at', 'admin_link')
    list_filter = ('media_type', 'uploaded_at')
    search_fields = ('file',)
    readonly_fields = ('preview', 'formatted_size', 'uploaded_at')
    fieldsets = (
        (None, {
            'fields': ('file', 'preview')
        }),
        ('Information', {
            'fields': ('media_type', 'formatted_size', 'uploaded_at')
        }),
    )

    def preview(self, obj):
        if obj.media_type == 'image':
            return mark_safe(f'<img src="{obj.file.url}" style="max-height: 100px; max-width: 150px;" />')
        elif obj.media_type == 'video':
            return mark_safe(f'''
                <video width="150" height="100" controls>
                    <source src="{obj.file.url}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            ''')
        return "Aucun aperçu disponible"
    preview.short_description = 'Aperçu'

    def name(self, obj):
        return obj.file.name.split('/')[-1]
    name.short_description = 'Nom du fichier'

    def formatted_size(self, obj):
        if obj.size < 1024:
            return f"{obj.size} octets"
        elif obj.size < 1024 * 1024:
            return f"{obj.size / 1024:.1f} Ko"
        else:
            return f"{obj.size / (1024 * 1024):.1f} Mo"
    formatted_size.short_description = 'Taille'

    def admin_link(self, obj):
        url = reverse('admin:core_mediafile_change', args=[obj.id])
        return mark_safe(f'<a href="{url}">Éditer</a>')
    admin_link.short_description = 'Action'