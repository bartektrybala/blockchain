# Generated by Django 4.2.2 on 2023-06-08 21:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blockchain", "0004_alter_block_previous_hash"),
    ]

    operations = [
        migrations.AlterField(
            model_name="block",
            name="timestamp",
            field=models.DateTimeField(),
        ),
    ]
