# Generated by Django 2.2.1 on 2022-03-13 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pare_central', '0004_auto_20220313_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseprofile',
            name='lastActive',
            field=models.CharField(default='11:05PM', max_length=25),
        ),
    ]
