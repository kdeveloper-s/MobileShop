# Generated by Django 3.2.6 on 2021-08-15 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MobilePhone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('color1', models.CharField(max_length=50)),
                ('color2', models.CharField(max_length=50)),
                ('color3', models.CharField(max_length=50)),
                ('camera_resolution', models.IntegerField()),
            ],
        ),
    ]