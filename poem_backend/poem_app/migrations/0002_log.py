# Generated by Django 2.2.1 on 2019-06-23 03:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poem_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(default='', max_length=11)),
                ('poem', models.TextField(blank=True, max_length=255, null=True)),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
