# Generated by Django 3.1.4 on 2021-01-11 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0008_auto_20210111_2141'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='lesson',
            name='is_invoiced',
            field=models.BooleanField(default=False),
        ),
    ]
