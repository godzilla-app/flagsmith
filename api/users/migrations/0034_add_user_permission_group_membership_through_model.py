# Generated by Django 3.2.18 on 2023-03-22 16:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0033_ffadminuser_sign_up_type'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='UserPermissionGroupMembership',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('ffadminuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                        ('userpermissiongroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userpermissiongroup')),
                    ],
                    options={
                        'db_table': 'users_userpermissiongroup_users',
                    },
                ),
                migrations.AlterField(
                    model_name='userpermissiongroup',
                    name='users',
                    field=models.ManyToManyField(blank=True, related_name='permission_groups', through='users.UserPermissionGroupMembership', to=settings.AUTH_USER_MODEL),
                ),
            ],
            database_operations=[]
        ),
        migrations.AddField(
            model_name="UserPermissionGroupMembership",
            name="group_admin",
            field=models.BooleanField(default=False),
        )
    ]
