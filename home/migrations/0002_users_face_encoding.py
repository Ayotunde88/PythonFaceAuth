# Generated by Django 5.1.1 on 2024-09-11 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='face_encoding',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
