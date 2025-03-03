from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Project, Tag, Category, User
from .forms import ProjectForm, UserForm
from django.urls import reverse_lazy



###############################################################################################
# Project CRUD CBV
###############################################################################################
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

###############################################################################################
# User CRUD CBV
###############################################################################################
class UserListView(ListView):
    model = User
    template_name = 'user/user-view.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'user/user-create.html'
    success_url = reverse_lazy('user_list')

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/user-update.html'
    success_url = reverse_lazy('user_list')


class UserDeleteView(DeleteView):
    model = User
    template_name = 'user/user-delete.html'
    success_url = reverse_lazy('user_list')
    
class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'
