# Generated by Django 5.0.6 on 2024-07-13 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0005_activeuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='activeuser',
            name='user_id',
            field=models.IntegerField(default=int),
        ),
    ]
