
from django import forms
from .models import Project
# Project Form 

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'total_target', 'start_time', 'end_time', 'category', 'tags']
