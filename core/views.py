from django.shortcuts import render, redirect
from .forms import MediaFileForm
from .models import MediaFile
from django.contrib import messages

def upload_media(request):
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Fichier uploadé avec succès!")
                return redirect('upload_media')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = MediaFileForm()
    
    media_files = MediaFile.objects.all().order_by('-uploaded_at')[:10]
    return render(request, 'core/upload.html', {
        'form': form,
        'media_files': media_files,
    })
    
def home(request):
    recent_media = MediaFile.objects.all().order_by('-uploaded_at')[:6]
    return render(request, 'core/home.html', {'recent_media': recent_media})

