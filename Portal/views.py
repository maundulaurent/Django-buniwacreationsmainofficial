# Portal/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from Buniwa.models import UserDetails
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.template.loader import render_to_string


@login_required
@require_POST
def toggle_milestone_status(request, milestone_id):
    milestone = get_object_or_404(Milestone, id=milestone_id)
    milestone.completed = not milestone.completed
    milestone.save()
    return redirect('create_milestones', request_id=milestone.project.id)

from django.http import JsonResponse


@login_required
def client_portal(request):
    if request.method == 'POST':
        form = ProjectRequestForm(request.POST)
        if form.is_valid():
            project_request = form.save(commit=False)
            project_request.user = request.user
            project_request.status = 'Requested'
            project_request.save()
            return redirect('client_portal')
    else:
        form = ProjectRequestForm()

    pending_projects = ProjectRequest.objects.filter(user=request.user, status='Requested')
    active_projects = ProjectRequest.objects.filter(user=request.user, status='In Progress')
    completed_projects = ProjectRequest.objects.filter(user=request.user, status='Completed')

    active_tasks = Milestone.objects.filter(project__in=active_projects, completed=False)
    completed_tasks = Milestone.objects.filter(project__in=completed_projects, completed=True)

        # Fetch user details
    user_details = UserDetails.objects.get(user=request.user)

    return render(request, 'Portal/client_portal.html', {
        'form': form,
        'pending_projects': pending_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'active_tasks': active_tasks,
        'completed_tasks': completed_tasks,
        'user_details': user_details,
    })


@login_required
def project_details(request, project_id):
    project = get_object_or_404(ProjectRequest, id=project_id, user=request.user)
    milestones = Milestone.objects.filter(project=project)

    return render(request, 'Portal/project_details.html', {
        'project': project,
        'milestones': milestones,
    })



def is_admin(user):
    return user.is_superuser  # Ensure only admins can access this view



@login_required
@user_passes_test(is_admin)
def admin_portal(request):
    project_requests = ProjectRequest.objects.all()

    return render(request, 'Portal/admin_portal.html', {
        'project_requests': project_requests,
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('client_portal')
        else:
            # Handle invalid login attempt
            return render(request, 'Portal/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'Portal/login.html')


@user_passes_test(is_admin)
def accept_request(request, request_id):
    project_request = get_object_or_404(ProjectRequest, id=request_id)
    project_request.status = 'In Progress'
    project_request.save()
    return redirect('admin_portal')



@login_required
def create_milestones(request, request_id):
    project_request = get_object_or_404(ProjectRequest, id=request_id)

    if request.method == 'POST':
        if 'accept_request' in request.POST:
            project_request.status = 'In Progress'
            project_request.save()
            return JsonResponse({'success': True, 'status': 'In Progress'})

        elif 'complete_project' in request.POST:
            project_request.status = 'Completed'
            project_request.save()
            return JsonResponse({'success': True, 'status': 'Completed'})

        else:
            form = MilestoneForm(request.POST, request.FILES)
            if form.is_valid():
                milestone = form.save(commit=False)
                milestone.project = project_request
                milestone.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = MilestoneForm()

    milestones = Milestone.objects.filter(project=project_request)
    all_milestones_complete = all(milestone.completed for milestone in milestones)

    return render(request, 'Portal/create_milestones.html', {
        'form': form,
        'milestones': milestones,
        'project_request': project_request,
        'request_id': request_id,
        'all_milestones_complete': all_milestones_complete,
    })



@login_required
@require_POST
def toggle_milestone_status(request, milestone_id):
    milestone = get_object_or_404(Milestone, id=milestone_id)
    milestone.completed = not milestone.completed
    milestone.save()
    return redirect('create_milestones', request_id=milestone.project.id)

@login_required
def edit_milestone(request, milestone_id):
    milestone = get_object_or_404(Milestone, id=milestone_id)

    if request.method == 'POST':
        form = MilestoneForm(request.POST, request.FILES, instance=milestone)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = MilestoneForm(instance=milestone)

    return JsonResponse({
        'form': form.as_p(),
        'milestone_id': milestone_id,
        'image_url': milestone.image.url if milestone.image else None,
    })

@login_required
def delete_milestone(request, milestone_id):
    milestone = get_object_or_404(Milestone, id=milestone_id)
    milestone.delete()
    return redirect('create_milestones', request_id=milestone.project.id)

@login_required
def complete_project(request, request_id):
    project_request = get_object_or_404(ProjectRequest, id=request_id)
    project_request.status = 'Completed'
    project_request.save()
    return redirect('admin_portal')  # Or another page where the admin can view the project details


def change_to_progress(request, project_id):
    project = get_object_or_404(ProjectRequest, id=project_id)

    if request.method == "POST":
        # Change project status to 'In Progress'
        project.status = 'In Progress'
        project.save()
        
        # Fetch existing milestones for the project
        milestones = Milestone.objects.filter(project=project)

        # Check if there are any milestones
        if milestones.exists():
            # Prepare a new milestone form to add more milestones if needed
            form = MilestoneForm()
        else:
            # If no milestones exist, prepare the form to create new milestones
            form = MilestoneForm()
        
        return render(request, 'Portal/create_milestones.html', {
            'form': form,
            'milestones': milestones,
            'project_request': project,
            'all_milestones_complete': False  # No way to be complete if there are no milestones
        })
    
    return redirect('project_details', project_id=project.id) 

@login_required
def client_project_details(request, request_id):
    project_request = get_object_or_404(ProjectRequest, id=request_id)
    milestones = Milestone.objects.filter(project=project_request)

    return render(request, 'Portal/client_project_details.html', {
        'project_request': project_request,
        'milestones': milestones,
    })