# Generated by Django 5.0.7 on 2024-07-26 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0003_remove_tweet_media'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweet',
            old_name='image',
            new_name='media',
        ),
    ]
