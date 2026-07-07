from django.db import models


# Stores one student record in the database.
class Student(models.Model):
    # Unique school registration number.
    registration_number = models.CharField(max_length=50, unique=True)

    # Basic personal details.
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    # Academic details.
    course = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        # Text shown for this student in admin and shell.
        return f"{self.first_name} {self.last_name}"
