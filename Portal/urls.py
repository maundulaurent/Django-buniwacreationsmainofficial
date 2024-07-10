from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_portal, name='client_portal'),
    path('admin/', views.admin_portal, name='admin_portal'),
    path('admin/approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('admin/add_milestone/<int:request_id>/', views.add_milestone, name='add_milestone'),
    path('admin/view_project_details/<int:request_id>/', views.view_project_details, name='view_project_details'),
    path('admin/complete_project/<int:request_id>/', views.complete_project, name='complete_project'),
    path('chat/', views.chat, name='chat'),  # Add this line
]
