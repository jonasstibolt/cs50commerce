# Generated by Django 3.2.3 on 2024-09-28 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20240928_0821'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]