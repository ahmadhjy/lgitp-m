from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import uuid
from django.conf import settings


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(published=True).order_by('-created_at')
    serializer_class = PostSerializer


@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('file')
        if image:
            # Generate a unique filename using UUID
            filename = str(uuid.uuid4()) + os.path.splitext(image.name)[1]
            file_path = os.path.join('blogs/uploads/', filename)

            try:
                # Save the file to the specified location
                saved_path = default_storage.save(file_path, ContentFile(image.read()))
                file_url = os.path.join(settings.MEDIA_URL, saved_path)

                # Return the file URL in the JSON response
                return JsonResponse({'location': file_url})

            except Exception as e:
                # Handle any exceptions that occur during the file save process
                return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Image upload failed'}, status=400)