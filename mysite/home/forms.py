from django import forms 
from .models import Certi
from .models import Orders
from .models import Contact
from .models import Project

class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['name','adnum','certi_name', 'drivelink', 'certi_no', 'start_date', 'end_date', 'credits','certificate']

class certiform(forms.ModelForm):
    is_approved = forms.BooleanField(label='Is Approved?', required=False)
    class Meta:
        model = Certi
        fields = ['type','event_name','event_link','event_start_date','event_end_date']

class contactform(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['fullname','branch','stdyear','phno','git','linkedin','hrank','aadhar','addr','adnum','section']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_link', 'description', 'start_date', 'end_date','branch','section','domain']

# home/forms.py
from django import forms
from .models import Mentor

class MentorForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = ['full_name', 'email']  # Include fields you want in the form

