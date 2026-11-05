from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Review(models.Model):
    first_n = models.CharField(max_length=30)
    last_n = models.CharField(max_length=30)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])