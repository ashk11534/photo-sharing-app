# Generated by Django 4.1 on 2022-08-19 16:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0012_remove_profile_followers_remove_profile_following_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="message_receiver",
                        to="base.profile",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="message_sender",
                        to="base.profile",
                    ),
                ),
            ],
        ),
    ]
