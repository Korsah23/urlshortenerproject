# Generated by Django 4.1.3 on 2022-11-24 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Urls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userLink', models.CharField(max_length=10000)),
                ('uuid', models.CharField(max_length=20)),
            ],
        ),
    ]
