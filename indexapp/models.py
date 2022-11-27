from django.db import models

# Create your models here.


class Admission(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    desctiption = models.CharField(max_length=255)
    email= models.EmailField()
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.email