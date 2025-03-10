from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

SEC=(
    ( 'A', 'A' ),
    ('B','B'),
    ('C', 'C'),
)

BRANCH = (
    ( 'CSE', 'CSE'),
    ('CSE-CS', 'CSE-CS'),
    ('CSE-AI-DS', 'CSE-AI-DS'),
    ('CSE-AI-ML', 'CSE-AI-ML'),
    ('IT', 'IT'),
    ('ECE', 'ECE'),
    ('EEE', 'EEE'),
    ('MECH', 'MECH'),
)

class Contact(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    fullname = models.CharField(max_length=60)
    branch = models.CharField(max_length=100,choices=BRANCH,null=True)
    stdyear = models.CharField(max_length=6)
    phno = models.CharField(max_length=12)
    git = models.CharField(max_length=100)
    linkedin = models.CharField(max_length=100)
    hrank = models.CharField(max_length=100)
    aadhar = models.CharField(max_length=16)
    addr = models.TextField()
    adnum=models.CharField(max_length=11)
    image = models.ImageField(default='mysite\templates\avatar.jpg',upload_to='contact_images')
    section = models.CharField(max_length=100,choices=SEC,null=True)
    def __str__(self):
        return f'{self.fullname}-{self.adnum}'


CATEGORY=(
    ('Web Development','web development'),
    ('hello world','helloworld'),
)
TYPES=(
    ('nptel','nptel'),
    ('workshops','workshops'),
    ('webinar','webinar'),
    ('sports','sports'),
    ('exams','exams'),
    ('certifications','certifications'),
    ('internships','internships'),
    ('hackathon','hackathon'),
    ('Technical','Technical'),
    ('others','others'),
)
LEVELS=(
    ( 'easy', 'easy' ),
    ('moderate','moderate'),
    ('hard', 'hard'),
)
DOMAIN=(
    ( 'DataScience', 'DataScience' ),
    ('ML','ML'),
    ('GenAI', 'GenAI'),
    ('Frontend', 'Frontend'),
    ('Backend', 'Backend'),
    ('Fullstack', 'Fullstack'),
    ('AppDevelopment', 'AppDevelopment'),
    ('CyberSecurity', 'CyberSecurity'),
    ('CloudComputing', 'CloudComputing'),
    ('Networking', 'Networking'),
    ('IOT', 'IOT'),
    ('EmbeddedSystems', 'EmbeddedSystems'),
    ('Robotics', 'Robotics'),
    ('AI', 'AI'),
    ('AR/VR', 'AR/VR'),
    ('GameDevelopment', 'GameDevelopment'),
    ('QuantumComputing', 'QuantumComputing'),
    ('Blockchain', 'Blockchain'),
    ('DevOps', 'DevOps'),
    ('Testing', 'Testing'),
    ('Database', 'Database'),
    ('BigData', 'BigData'),
    ('WebDevelopment', 'WebDevelopment'),
    ('Others', 'Others'),
)



class Certi(models.Model):
    type = models.CharField(max_length=100, choices=TYPES, null=True)
    # category = models.CharField(max_length=20, choices=CATEGORY)
    event_name = models.CharField(max_length=75, null=True)
    event_link = models.CharField(max_length=75, null=True)
    event_start_date = models.DateField(null=True)
    event_end_date = models.DateField(null=True)
    is_approved = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='certi_registrations')

    def get_registrations(self):
        return Registration.objects.filter(event=self)

    def get_registration_count(self):
        return self.get_registrations().count()


class Registration(models.Model):
    event = models.ForeignKey(Certi, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.event.event_name}'

class Orders(models.Model):
    adnum=models.CharField(max_length=10,null=True)
    name = models.CharField(max_length=75,null=True)
    staff = models.ForeignKey(User,models.CASCADE,null=True)
    certi_name = models.CharField(max_length=100)
    drivelink = models.CharField(max_length=100)
    certi_no = models.CharField(max_length=100)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    credits = models.PositiveIntegerField(null=True)
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)
    def __str__(self):
        return f'{self.certi_name}-{self.drivelink}'
    


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    project_link = models.URLField()
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    branch = models.CharField(max_length=100,choices=BRANCH,null=True)
    section = models.CharField(max_length=100,choices=SEC,null=True)
    domain = models.CharField(max_length=100,choices=DOMAIN,null=True)
    
    def __str__(self):
        return self.project_name
    
class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relation with User
    full_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.full_name

class Team(models.Model):
    name = models.CharField(max_length=100)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)  # Each team has a mentor
    members = models.ManyToManyField(Contact, related_name='teams')  # Students assigned to a team

    def __str__(self):
        return f'{self.name} - {self.mentor.full_name}'

class ProgressReport(models.Model):
    student = models.ForeignKey(Contact, on_delete=models.CASCADE)  # Link to a student (Contact)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # Link to a project
    report_title = models.CharField(max_length=200)
    report_description = models.TextField()
    status_choices = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='not_started')
    date_submitted = models.DateTimeField(default=timezone.now)  # Timestamp of when the report was submitted

    def __str__(self):
        return f'{self.student.fullname} - {self.report_title}'
