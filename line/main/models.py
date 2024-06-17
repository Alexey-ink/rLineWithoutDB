from django.db import models

# Create your models here.

from django.db import models

class UserRequest(models.Model):
    text = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
