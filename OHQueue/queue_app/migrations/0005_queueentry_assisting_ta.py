# Generated by Django 4.1.13 on 2023-11-28 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queue_app', '0004_queueentry_creation_date_queueentry_in_queue_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='queueentry',
            name='assisting_ta',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
