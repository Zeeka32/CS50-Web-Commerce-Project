# Generated by Django 4.0.4 on 2023-04-09 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auctionlisting_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='bidders',
            field=models.IntegerField(default=0),
        ),
    ]