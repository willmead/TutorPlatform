# Generated by Django 3.1.5 on 2023-02-01 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0018_student_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
