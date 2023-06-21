from django.contrib import admin
import os

# Register your models here.
from .models import Lockedfiles

#admin.site.register(Document)


class LockedAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        if obj.file:
            file_path = obj.file.path
            if os.path.exists(file_path):
                os.remove(file_path)
        super().delete_model(request, obj)

admin.site.register(Lockedfiles, LockedAdmin)