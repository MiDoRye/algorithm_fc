# Generated by Django 4.2.1 on 2023-05-09 05:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_user_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="image",
            field=models.ImageField(upload_to=""),
        ),
    ]