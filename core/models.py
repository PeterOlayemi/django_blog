from django.db import models

# Create your models here.

class ContactMessage(models.Model):
    name = models.CharField(max_length=99)
    email = models.EmailField(max_length=99)
    subject = models.CharField(max_length=99)
    message = models.TextField(max_length=499)

    def __str__(self):
        return f"Name: {self.name}; Subject: {self.subject}"
