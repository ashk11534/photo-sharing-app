# Generated by Django 4.1 on 2022-08-20 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0014_message_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="body",
            field=models.TextField(blank=True, null=True),
        ),
    ]
