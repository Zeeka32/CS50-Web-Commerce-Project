# Generated by Django 4.0.4 on 2023-04-09 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auctionlisting_date_bid_bidders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='date_modified',
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_created',
            field=models.DateField(auto_now=True),
        ),
    ]
