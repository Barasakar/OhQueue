# Generated by Django 4.1.13 on 2023-11-27 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queue_app', '0002_alter_customuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueueEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('question', models.TextField()),
                ('location', models.CharField(max_length=100)),
            ],
        ),
    ]
