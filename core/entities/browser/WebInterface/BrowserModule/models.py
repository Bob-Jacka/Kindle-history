from django.db import models


class Books(models.Model):
    name = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Book_manufacturers(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
