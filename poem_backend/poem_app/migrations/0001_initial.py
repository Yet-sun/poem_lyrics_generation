# Generated by Django 2.2.1 on 2019-06-16 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(default='', max_length=20)),
                ('password', models.CharField(default='123456', max_length=20)),
            ],
        ),
    ]