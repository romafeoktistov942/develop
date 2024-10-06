# Generated by Django 4.2.15 on 2024-10-05 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_version"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="version",
            options={
                "ordering": ["version_number"],
                "verbose_name": "Версия",
                "verbose_name_plural": "Версии",
            },
        ),
        migrations.RemoveField(
            model_name="version",
            name="name",
        ),
        migrations.RemoveField(
            model_name="version",
            name="number",
        ),
        migrations.AddField(
            model_name="version",
            name="version_name",
            field=models.CharField(
                default="Новая версия", max_length=255, verbose_name="Название версии"
            ),
        ),
        migrations.AddField(
            model_name="version",
            name="version_number",
            field=models.IntegerField(default=1.0, verbose_name="Номер версии"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="version",
            name="is_active",
            field=models.BooleanField(
                default=False, verbose_name="Признак текущей версии"
            ),
        ),
        migrations.AlterField(
            model_name="version",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="catalog.product"
            ),
        ),
    ]
