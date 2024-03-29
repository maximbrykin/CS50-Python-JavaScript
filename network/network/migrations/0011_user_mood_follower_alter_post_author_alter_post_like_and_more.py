# Generated by Django 4.0.4 on 2022-07-21 04:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mood',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follow', models.ManyToManyField(blank=True, related_name='followed', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='network.follower'),
        ),
        migrations.AlterField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='liked', to='network.follower'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
