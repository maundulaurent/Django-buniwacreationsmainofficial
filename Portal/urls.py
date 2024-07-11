# Portal/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.client_portal, name='client_portal'),
    path('login/', views.login_view, name='login'),  # Simple login view
    path('admin/', views.admin_portal, name='admin_portal'),  # Admin portal view
    path('accept_request/<int:request_id>/', views.accept_request, name='accept_request'),  # Accept Request
    path('create_milestones/<int:request_id>/', views.create_milestones, name='create_milestones'),  # Create Milestones
    path('complete_project/<int:request_id>/', views.complete_project, name='complete_project'),  # Complete Project
    # path('logout/', auth_views.LogoutView.as_view(next_page='client_portal'), name='logout'),
    path('reply_message/<int:user_id>/', views.reply_message, name='reply_message'),
]
