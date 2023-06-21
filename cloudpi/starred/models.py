# starred/models.py
from django.db import models

class Starred(models.Model):
    name = models.CharField(max_length=255)
    is_starred = models.BooleanField(default=False)

    def _str_(self):
        return self.name