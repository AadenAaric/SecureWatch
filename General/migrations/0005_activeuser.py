# Generated by Django 5.0.6 on 2024-07-12 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('General', '0004_remove_user_groups_remove_user_is_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashed_id', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
