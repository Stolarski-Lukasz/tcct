from django.db import models

# Create your models here.

class Conversions(models.Model):
    text_sample = models.TextField(max_length=500)
    text_length = models.IntegerField()
    date_time = models.DateTimeField(auto_now_add=True)
