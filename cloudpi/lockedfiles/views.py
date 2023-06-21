from django.shortcuts import render
import os
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Lockedfiles
from .serializers import LockedFSerializer
from rest_framework.parsers import MultiPartParser,FormParser
from io import BytesIO
from django.conf import settings
from django.core.files.storage import default_storage
from pdf2image import convert_from_path

# Create your views here.
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def locked_view_upload(request):
    if request.method == 'GET':
        locked = Lockedfiles.objects.all()
        serializer = LockedFSerializer(locked, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = LockedFSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':  # New section to handle viewing a specific document
        locked_id = request.data.get('locked_id')
        if locked_id:
            try:
                locked = Lockedfiles.objects.get(id=locked_id)
                # Perform any additional operations you need with the document
                # For example, you can return the document data or redirect to a download URL
                serializer = LockedFSerializer(locked)
                return Response(serializer.data)
            except Lockedfiles.DoesNotExist:
                return Response({'error': 'lockedfile not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Missing lockedfile_id parameter'}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['DELETE'])
def locked_delete(request, pk):
    try:
        locked = Lockedfiles.objects.get(pk=pk)
    except Lockedfiles.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        file_path=locked.file.path
        #print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        locked.delete()


        return Response(status=status.HTTP_204_NO_CONTENT)