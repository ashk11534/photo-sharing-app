# Generated by Django 4.1 on 2022-08-14 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_alter_profile_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="profile_image",
            field=models.ImageField(
                default="user-images/avatar.png", upload_to="user-images/"
            ),
        ),
    ]
