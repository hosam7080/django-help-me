from django.urls import path
from fund.views import *
from django.contrib.auth.decorators import login_required as LR
from django.contrib.auth import views as auth_views
from fund.forms import LoginForm


urlpatterns = [
		###############################################################################################
		####################################### Project CRUD CBV ######################################
		###############################################################################################
    path('projects/', LR(ProjectListView.as_view()), name='project_list'),
    path('projects/create/', LR(ProjectCreateView.as_view()), name='project_create'),
    path('projects/<int:pk>/update/', LR(ProjectUpdateView.as_view()), name='project_update'),
    path('projects/<int:pk>/delete/', LR(ProjectDeleteView.as_view()), name='project_delete'),
    path('projects/<int:pk>/', LR(ProjectDetailView.as_view()), name='project_detail'),
		path('projects/<int:pk>/donation/', LR(DonateProject.as_view()), name='project_donate'),
		path('projects/<int:pk>/comment/', LR(CommentProject.as_view()), name='project_comment'),


		###############################################################################################
		####################################### User CRUD CBV #########################################
		###############################################################################################
    path('users/update/<int:pk>/', LR(UserUpdateView.as_view()), name='user_update'),
    path('users/delete/<int:pk>/', LR(UserDeleteView.as_view()), name='user_delete'),
    path('users/<int:pk>/', LR(UserDetailView.as_view()), name='user_detail'),
		path('user/activate/', ActivateUser.as_view(), name='user_activate'),


		###############################################################################################
		####################################### Core CBV #########################################
		###############################################################################################
    path('', HomeView.as_view(), name='home'),
		path('login/', auth_views.LoginView.as_view(template_name='core/signin.html', authentication_form=LoginForm), name='signin'),
		path('logout/', auth_views.LogoutView.as_view(template_name='core/signin.html'), name='signout'),
		path('signup/', SignupView.as_view(), name='signup'),
  
  
  ############## new ADDitions ########
	path("report/project/<int:project_pk>/", report_item, name="report_project"),
    path("report/comment/<int:project_pk>/<int:comment_pk>/", report_item, name="report_comment"),
    path("rate/project/<int:project_pk>//", rate_project, name="rate_project"),
    path("category/<int:category_pk>/", projects_by_category, name="projects_by_category"),
]
