# Generated by Django 2.2.1 on 2022-03-14 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pare_central', '0009_auto_20220314_0129'),
    ]

    operations = [
        migrations.AddField(
            model_name='twousermessage',
            name='key',
            field=models.CharField(default='', max_length=255),
        ),
    ]
