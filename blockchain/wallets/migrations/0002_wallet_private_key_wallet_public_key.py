# Generated by Django 4.2.2 on 2023-06-08 10:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wallets", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="wallet",
            name="private_key",
            field=models.BinaryField(max_length=32, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="wallet",
            name="public_key",
            field=models.BinaryField(max_length=32, null=True, unique=True),
        ),
    ]