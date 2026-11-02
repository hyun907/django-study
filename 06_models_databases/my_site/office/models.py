from django.db import models

# Create your models here.
class Patient(models.Model):
    first_n = models.CharField(max_length=30)
    last_n = models.CharField(max_length=30)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.last_n}, {self.first_n}, is {self.age} years old"