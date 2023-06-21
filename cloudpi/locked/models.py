from django.contrib.auth import get_user_model
from django.db import models

user = get_user_model()


class Locked(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    mail = models.EmailField()
    otp = models.CharField(max_length=6)

    def _str_(self):
        return f"{self.mail} - {self.user.username}"
