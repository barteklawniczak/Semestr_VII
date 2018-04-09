from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from .validators import validate_file_extension


class File(models.Model):
    title = models.CharField(max_length=100, blank=True, unique=True)
    uploaded_path = models.FileField(upload_to='./',  validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visualisations = models.BooleanField(default=False)

    def retrieve_index(self):
        return self.title.lower().split('.')[0]


class ToolsDone(models.Model):
    isDone = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    port = models.BigIntegerField(default=0)
