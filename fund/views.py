from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from .models import *
from .forms import ProjectForm, SignupForm, UserUpdateForm
from django.urls import reverse_lazy
from django.db.models import Avg, Sum, Q, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone
import random
import string
import requests


###############################################################################################
####################################### Project CRUD CBV ######################################
###############################################################################################
class ProjectListView(ListView):
	model = Project
	template_name = 'project/project_list.html'
	context_object_name = 'projects'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		context['tags'] = Tag.objects.all()

		projects = Project.objects.filter(end_time__gt=timezone.now()).annotate(
			total_donation=Coalesce(Sum('donations__amount'), 0, output_field=DecimalField()),
			avg_rating=Coalesce(Avg('rating__rate'), 0, output_field=DecimalField())
		)
		context["projects"] = projects
		return context


class ProjectCreateView(CreateView):
	model = Project
	form_class = ProjectForm
	template_name = 'project/project_list.html'
	success_url = reverse_lazy('project_list')

	def form_valid(self, form):
		form.instance.owner = self.request.user
		response = super().form_valid(form)
		images = self.request.FILES.getlist('images') 
		for image in images:
			Picture.objects.create(project=self.object, image=image)

		return response


class ProjectUpdateView(UpdateView):
	model = Project
	form_class = ProjectForm
	template_name = 'project/project_form.html'
	success_url = reverse_lazy('project_list')

	def form_valid(self, form):
		form.instance.owner = self.request.user
		response = super().form_valid(form)
		images = self.request.FILES.getlist('images') 
		for image in images:
			Picture.objects.create(project=self.object, image=image)

		return response


class ProjectDeleteView(DeleteView):
	model = Project
	template_name = 'base/delete_confirm.html'

	def get_success_url(self):
		return reverse_lazy('user_detail', kwargs={'pk': self.request.user.pk})

	def dispatch(self, request, *args, **kwargs):
		project = self.get_object()
		if project.owner != request.user:
			return redirect('user_detail', pk=request.user.pk)

		return super().dispatch(request, *args, **kwargs)


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


class DonateProject(View):
	def post(self, request, pk):
		project = get_object_or_404(Project, pk=pk)
		amount = request.POST.get("amount", 0.00)

		if float(amount) <= 0:
			return redirect('project_detail', pk=pk)

		Donation.objects.create(
			amount=float(amount),
			project=project,
			donated_by=request.user
		)
		return redirect('project_detail', pk=pk)


class CommentProject(View):
	def post(self, request, pk):
		project = get_object_or_404(Project, pk=pk)
		comment = request.POST.get('comment', None)
		
		if not comment:
			return redirect('project_detail', pk=pk)

		Comment.objects.create(
			content=comment,
			user=request.user,
			project=project
		)

		return redirect('project_detail', pk=pk)


###############################################################################################
####################################### User CRUD CBV #########################################
###############################################################################################
class UserUpdateView(UpdateView):
	model = User
	form_class = UserUpdateForm
	template_name = 'user/user-update.html'

	def get_success_url(self) -> str:
		return reverse('user_detail', args=[self.object.pk])


class UserDeleteView(DeleteView):
	model = User
	template_name = 'base/delete_confirm.html'

	def get_success_url(self):
		return reverse_lazy('signin')

	def dispatch(self, request, *args, **kwargs):
		user = self.get_object()
		if user != request.user:
			return redirect('user_detail', pk=request.user.pk)

		return super().dispatch(request, *args, **kwargs)


class UserDetailView(DetailView):
	model = User
	template_name = 'user/user-detail.html'
	context_object_name = 'user'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = self.get_object()
		projects = Project.objects.filter(owner=user).annotate(
			total_donation=Coalesce(Sum('donations__amount'), 0, output_field=DecimalField()),
			avg_rating=Coalesce(Avg('rating__rate'), 0, output_field=DecimalField())
		)

		donations = Donation.objects.filter(donated_by=user)

		context["projects"] = projects
		context["donations"] = donations
		return context


###############################################################################################
####################################### Core CRUD CBV #########################################
###############################################################################################
class HomeView(View):
	def get(self, request):
		projects = Project.objects.annotate(
			total_donation=Coalesce(Sum('donations__amount'), 0, output_field=DecimalField()),
			avg_rating=Coalesce(Avg('rating__rate'), 0, output_field=DecimalField())
		)

		highest_rated_projects = projects.filter(avg_rating__gt=0).order_by('-avg_rating')[:5]
		highest_donated_projects = projects.filter(total_donation__gt=0).order_by('-total_donation')[:5]
		latest_projects = projects.order_by('-created_at')[:5]
		featured_projects = projects.filter(featuerd=True).order_by('-created_at')[:5]
		categories = Category.objects.all().order_by('name')

		query = request.GET.get('q')
		search_results = None
		if query:
			search_results = Project.objects.filter(
				Q(title__icontains=query) | Q(tags__name__icontains=query)
			).distinct()

		context = {
			'highest_rated_projects': highest_rated_projects,
			'highest_donated_projects': highest_donated_projects,
			'latest_projects': latest_projects,
			'featured_projects': featured_projects,
			'categories': categories,
			'search_results': search_results,
			'query': query,
		}
		return render(request, 'base/homepage.html', context)


class SignupView(View):
	def generate_random_string(self, length=30):
		characters = string.ascii_letters + string.digits
		return ''.join(random.choices(characters, k=length))

	def get(self, request):
		form = SignupForm()
		return render(request, 'core/signup.html', {
			'form': form,
			"dont_show_navbar": True
		})

	def post(self, request):
		form = SignupForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()

			token = self.generate_random_string()
			Token.objects.create(
				token=token,
				user=form.instance
			)

			form.instance.is_active = False
			form.instance.save()

			requests.get(url=f"https://salesprogrow.com/api/email/?token={token}&email={form.instance.email}&user={form.instance.pk}")

			return redirect('signin')

		else:
			return render(request, 'core/signup.html', {'form': form})


class ActivateUser(View):
	def get(self, request):
		user_id = request.GET.get('user')
		token = request.GET.get('token')

		if not user_id or not token:
			return HttpResponse("Not allowed")
		
		user = User.objects.get(id=int(user_id))
		q = Token.objects.filter(token=token, user=user)
		if q.exists():
			user.is_active=True
			user.save()

			return redirect('signin')

		return HttpResponse("Not allowed")



