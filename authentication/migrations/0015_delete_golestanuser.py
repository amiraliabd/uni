# Generated by Django 4.2 on 2023-09-15 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_alter_pendingevaluation_unique_together_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GolestanUser',
        ),
    ]
