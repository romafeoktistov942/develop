# Generated by Django 4.2.15 on 2024-09-05 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="manufactured_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
