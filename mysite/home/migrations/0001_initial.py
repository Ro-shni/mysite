# Generated by Django 4.2.16 on 2024-11-05 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Certi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('nptel', 'nptel'), ('workshops', 'workshops'), ('webinar', 'webinar'), ('sports', 'sports'), ('exams', 'exams'), ('certifications', 'certifications'), ('internships', 'internships'), ('hackathon', 'hackathon'), ('Technical', 'Technical'), ('others', 'others')], max_length=100, null=True)),
                ('event_name', models.CharField(max_length=75, null=True)),
                ('event_link', models.CharField(max_length=75, null=True)),
                ('event_start_date', models.DateField(null=True)),
                ('event_end_date', models.DateField(null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_completed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='certi_registrations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_registered', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.certi')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adnum', models.CharField(max_length=10, null=True)),
                ('name', models.CharField(max_length=75, null=True)),
                ('certi_name', models.CharField(max_length=100)),
                ('drivelink', models.CharField(max_length=100)),
                ('certi_no', models.CharField(max_length=100)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('credits', models.PositiveIntegerField(null=True)),
                ('certificate', models.FileField(blank=True, null=True, upload_to='certificates/')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=60)),
                ('branch', models.CharField(choices=[('CSE', 'CSE'), ('CSE-CS', 'CSE-CS'), ('CSE-AI-DS', 'CSE-AI-DS'), ('CSE-AI-ML', 'CSE-AI-ML'), ('IT', 'IT'), ('ECE', 'ECE'), ('EEE', 'EEE'), ('MECH', 'MECH')], max_length=100, null=True)),
                ('stdyear', models.CharField(max_length=6)),
                ('phno', models.CharField(max_length=12)),
                ('git', models.CharField(max_length=100)),
                ('linkedin', models.CharField(max_length=100)),
                ('hrank', models.CharField(max_length=100)),
                ('aadhar', models.CharField(max_length=16)),
                ('addr', models.TextField()),
                ('adnum', models.CharField(max_length=11)),
                ('image', models.ImageField(default='mysite\templates\x07vatar.jpg', upload_to='contact_images')),
                ('section', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=100, null=True)),
                ('staff', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
