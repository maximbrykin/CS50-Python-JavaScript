# Generated by Django 4.0.4 on 2022-07-20 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_rename_follower_follower_following'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mood', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='mood',
        ),
        migrations.DeleteModel(
            name='Follower',
        ),
        migrations.AddField(
            model_name='profile',
            name='follow',
            field=models.ManyToManyField(blank=True, related_name='followed', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
