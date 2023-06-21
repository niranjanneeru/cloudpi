from django.db import models

class Lockedfiles(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='locked/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
