# Generated by Django 5.0.1 on 2024-01-19 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_delete_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile',
            field=models.BooleanField(default=False),
        ),
    ]