# Generated by Django 3.2.14 on 2022-08-12 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_processor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthCheckModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.UUIDField(unique=True)),
            ],
        ),
    ]