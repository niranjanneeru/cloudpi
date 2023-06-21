from django.db import models

class Document(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='document/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_starred = models.BooleanField(default=False)

    def __str__(self):
        return self.name
