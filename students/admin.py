from django.contrib import admin
from .models import Student

# Makes Student records manageable in Django admin.
admin.site.register(Student)
