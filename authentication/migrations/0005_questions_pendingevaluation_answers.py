# Generated by Django 4.2 on 2023-05-26 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_user_password_alter_section_assistants_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('comment', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PendingEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pending_eval', to='authentication.questions')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pending_eval', to='authentication.section')),
            ],
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.PositiveIntegerField(blank=True, null=True)),
                ('comment', models.CharField(max_length=120)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='authentication.questions')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evals', to='authentication.section')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='authentication.user')),
            ],
        ),
    ]
