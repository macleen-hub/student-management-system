from django.db import models


class Student(models.Model):
    registration_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"