# Generated by Django 4.2 on 2023-04-21 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roll',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rolls', to='authentication.user'),
        ),
        migrations.AlterField(
            model_name='user',
            name='student_number',
            field=models.CharField(default=None, max_length=9, null=True, unique=True),
        ),
    ]