from django.db import models
from django.contrib.auth.models import User     



class urldb(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, null=False,blank=False)    
    url = models.URLField(max_length=200)
    short_url = models.CharField(max_length=100)
    title=models.CharField(max_length=20)
    time = models.DateTimeField(auto_now=True)

