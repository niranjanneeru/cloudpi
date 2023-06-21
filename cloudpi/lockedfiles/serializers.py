from rest_framework import serializers
from .models import Lockedfiles

class LockedFSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lockedfiles
        fields = '__all__'
