# Portal/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
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
    path('delete_milestone/<int:milestone_id>/', views.delete_milestone, name='delete_milestone'),
    path('edit_milestone/<int:milestone_id>/', views.edit_milestone, name='edit_milestone'),
    path('toggle_milestone_status/<int:milestone_id>/', views.toggle_milestone_status, name='toggle_milestone_status'),
    path('change_to_progress/<int:project_id>/', views.change_to_progress, name='change_to_progress'),
    path('project/<int:project_id>/', views.project_details, name='project_details'),
    path('get_messages/<str:username>/', views.get_messages, name='get_messages'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
