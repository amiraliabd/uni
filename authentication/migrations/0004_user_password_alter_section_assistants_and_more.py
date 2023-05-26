# Generated by Django 4.2 on 2023-04-28 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='asd', max_length=90),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='section',
            name='assistants',
            field=models.ManyToManyField(blank=True, related_name='assistant_sections', to='authentication.user'),
        ),
        migrations.AlterField(
            model_name='section',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='student_sections', to='authentication.user'),
        ),
        migrations.AlterField(
            model_name='section',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teaching_sections', to='authentication.user'),
        ),
    ]