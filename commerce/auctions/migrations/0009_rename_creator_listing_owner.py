# Generated by Django 4.0.4 on 2022-06-15 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_listing_creator_listing_wishers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='creator',
            new_name='owner',
        ),
    ]
