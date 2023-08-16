from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)


class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
