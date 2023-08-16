from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=255, verbose_name="Name")
    last_name = models.CharField(max_length=255, verbose_name="Surname")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Birth date")
    biography = models.TextField(null=True, blank=True, verbose_name="Biography")


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    publication_date = models.DateField(verbose_name="Publication date")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books", verbose_name="Author"
    )
