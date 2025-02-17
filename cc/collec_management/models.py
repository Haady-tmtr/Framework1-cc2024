from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Collec(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title
    


class Element(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    value = models.FloatField()
    quantity = models.IntegerField()
    date_ajout = models.DateTimeField(auto_now_add=True)
    collection = models.ForeignKey('Collec', on_delete=models.CASCADE, related_name="elements")

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title