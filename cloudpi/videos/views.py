import os
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from rest_framework import status
from cloudpi.starred.models import Starred
from .models import Videos
from .serializers import VideoSerializer
from rest_framework.parsers import MultiPartParser,FormParser
from io import BytesIO
from django.conf import settings
from django.core.files.storage import default_storage
from pdf2image import convert_from_path



@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser,FormParser])
def video_view_upload(request):
    if request.method == 'GET':
        videos = Videos.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def video_delete(request, pk):
    try:
        video = Videos.objects.get(pk=pk)
    except Videos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        is_starred = video.is_starred
        file_path=video.video.path
        #print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        video.delete()

        if is_starred:
            starred = request.user.starred_video.all()
            if video in starred:
                request.user.starred_videos.remove(video)

        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def add_to_starred(request, pk):
    try:
        video = Videos.objects.get(pk=pk)
    except Videos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if video.is_starred:
        starred_video=Starred.objects.get(video=video)
        starred_video.delete()
    else:
        starred_video = Starred(video=video)
        starred_video.save()

    video.is_starred = not video.is_starred
    video.save()

    return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import generics

from .models import Videos
from .serializers import VideoSerializer


class StarredVideoListView(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        queryset = Videos.objects.filter(is_starred=True)
        return queryset

class StarredVideoUpdateView(generics.UpdateAPIView):
    queryset = Videos.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'id'
    allowed_methods = ['PUT']

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        is_starred = instance.is_starred

        instance.is_starred = not is_starred
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
