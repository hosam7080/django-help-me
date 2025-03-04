from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import *
from .forms import ProjectForm, UserForm
from django.urls import reverse_lazy

## 
from django.db.models import Sum

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

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/Project_details.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.pictures.all()  
        context['total_donation'] = self.object.donations.aggregate(total=Sum('amount'))['total'] or 0.0
        context['comments'] = self.object.comments.all().order_by('-created_at')
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Donation => post
        if "donation" in request.POST:
            donation_amount = request.POST.get("donation_amount")
            if donation_amount:
                Donation.objects.create(
                    project=self.object,
                    amount=donation_amount,
                    donated_by=request.user  # Check for user (logged in or not)
                )
        # Comment => Post
        elif "comment" in request.POST:
            comment_text = request.POST.get("comment_text")
            if comment_text and request.user.is_authenticated:
                Comment.objects.create(
                    project=self.object,
                    user=request.user,
                    content=comment_text  
                )
        return redirect('project_detail', pk=self.object.pk)


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
