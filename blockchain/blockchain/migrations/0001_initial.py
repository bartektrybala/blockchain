# Generated by Django 4.2.2 on 2023-06-08 11:04

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wallets", "0002_wallet_private_key_wallet_public_key"),
    ]

    operations = [
        migrations.CreateModel(
            name="Block",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("previous_hash", models.BinaryField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "security_hashes",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.BinaryField(), size=None
                    ),
                ),
                ("proof", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=5, max_digits=15)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "block",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="blockchain.block",
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="received_transactions",
                        to="wallets.wallet",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_transactions",
                        to="wallets.wallet",
                    ),
                ),
            ],
        ),
    ]
