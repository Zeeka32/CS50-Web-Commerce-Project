# Generated by Django 4.0.4 on 2023-04-10 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_bid_auction_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='auctions',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.auctionlisting'),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]