# Generated by Django 4.2 on 2023-10-10 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_evaluation_delete_pendingevaluation_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evaluation',
            old_name='dead_line',
            new_name='deadline',
        ),
        migrations.AlterUniqueTogether(
            name='evaluation',
            unique_together={('section', 'deadline')},
        ),
    ]
