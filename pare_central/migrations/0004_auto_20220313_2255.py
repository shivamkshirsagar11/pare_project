# Generated by Django 2.2.1 on 2022-03-13 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pare_central', '0003_auto_20220313_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseprofile',
            name='lastActive',
            field=models.CharField(default='10:55PM', max_length=25),
        ),
    ]