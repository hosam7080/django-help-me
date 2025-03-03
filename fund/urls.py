from django.urls import path
from fund.views import *

urlpatterns = [
    path('user-list/', UserListView.as_view(), name='user_list'),
    path('user-create/', UserCreateView.as_view(), name='user_create'),
    path('user-update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user-delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('user-detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),

]
