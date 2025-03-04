from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.shortcuts import render
from .models import Project, Tag, Category, User
from .forms import ProjectForm, UserForm
from django.urls import reverse_lazy
from django.db.models import Avg, Sum
from django.db.models import Q



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
    
    
class homepage(View):
    def get(self, request):
        highest_rated_projects = Project.objects.filter(end_time__isnull=True).annotate(
        avg_rating=Avg('rating__rate')
        ).order_by('-avg_rating')[:5]
        
        highest_donated_projects = Project.objects.annotate(
        total_donation=Sum('donations__amount')
        ).order_by('-total_donation')[:5]
        print(highest_donated_projects)

        latest_projects = Project.objects.order_by('-created_at')[:5]

        featured_projects = Project.objects.filter(featuerd=True).order_by('-created_at')[:5]

        categories = Category.objects.all()

        query = request.GET.get('q')
        search_results = None
        if query:
            search_results = Project.objects.filter(
                Q(title__icontains=query) | Q(tags__name__icontains=query)
            ).distinct()
            
        

        context = {
            'highest_rated_projects': highest_rated_projects,
            'latest_projects': latest_projects,
            'featured_projects': featured_projects,
            'categories': categories,
            'search_results': search_results,
            'query': query,
            'highest_donated_projects': highest_donated_projects,
            
        }
        return render(request, 'base/homepage.html', context)
