import os
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from rest_framework import status
from cloudpi.starred.models import Starred
from .models import Music
from .serializers import MusicSerializer
from rest_framework.parsers import MultiPartParser,FormParser
from io import BytesIO
from django.conf import settings
from django.core.files.storage import default_storage
from pdf2image import convert_from_path
import pytesseract


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser,FormParser])
def music_view_upload(request):
    if request.method == 'GET':
        music = Music.objects.all()
        serializer = MusicSerializer(music, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def music_delete(request, pk):
    try:
        music = Music.objects.get(pk=pk)
    except Music.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        is_starred = music.is_starred
        file_path=music.music.path
        #print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        music.delete()

        if is_starred:
            starred = request.user.starred_music.all()
            if music in starred:
                request.user.starred_music.remove(music)

        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def add_to_starred(request, pk):
    try:
        music = Music.objects.get(pk=pk)
    except Music.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if music.is_starred:
        starred_music=Starred.objects.get(music=music)
        starred_music.delete()
    else:
        starred_music = Starred(music=music)
        starred_music.save()

    music.is_starred = not music.is_starred
    music.save()

    return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import generics

from .models import Music
from .serializers import MusicSerializer


class StarredMusicListView(generics.ListAPIView):
    serializer_class = MusicSerializer

    def get_queryset(self):
        queryset = Music.objects.filter(is_starred=True)
        return queryset

class StarredMusicUpdateView(generics.UpdateAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    lookup_field = 'id'
    allowed_methods = ['PUT']

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        is_starred = instance.is_starred

        instance.is_starred = not is_starred
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
