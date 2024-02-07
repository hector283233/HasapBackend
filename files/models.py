from django.db import models

# Create your models here.
class ProductFiles(models.Model):
    file = models.FileField(upload_to="files/filter/", null=True, blank=True)