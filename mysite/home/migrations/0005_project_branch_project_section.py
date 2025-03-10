# Generated by Django 4.2.16 on 2025-03-10 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_mentor_team_progressreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='branch',
            field=models.CharField(choices=[('CSE', 'CSE'), ('CSE-CS', 'CSE-CS'), ('CSE-AI-DS', 'CSE-AI-DS'), ('CSE-AI-ML', 'CSE-AI-ML'), ('IT', 'IT'), ('ECE', 'ECE'), ('EEE', 'EEE'), ('MECH', 'MECH')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='section',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=100, null=True),
        ),
    ]
