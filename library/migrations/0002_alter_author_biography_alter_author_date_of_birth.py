# Generated by Django 4.2.4 on 2023-08-16 14:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="biography",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="author",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
    ]
