from django.urls import reverse_lazy #redirections
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Project
from .forms import ProjectForm



# Prject CRUD CBV
class ProjectListView(ListView):
    model = Project
    template_name = 'project/ProjectForm.html'
    context_object_name = 'projects'

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/ProjectForm.html'
    success_url = reverse_lazy('project_list')

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/ProjectForm.html'
    success_url = reverse_lazy('project_list')

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'project/ProjectForm.html'
    success_url = reverse_lazy('project_list')
