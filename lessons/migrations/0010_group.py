# Generated by Django 3.1.4 on 2021-01-11 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0009_auto_20210111_2149'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
    ]
