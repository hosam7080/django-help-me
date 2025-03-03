from django.urls import reverse_lazy #redirections
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Project,Tag,Category
from .forms import ProjectForm



# Prject CRUD CBV
class ProjectListView(ListView):
    model = Project
    template_name = 'project/ProjectForm.html'
    context_object_name = 'projects'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context
    
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

