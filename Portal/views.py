# Portal/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

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
            project_request.status = 'Requested'  # Set default status to 'Requested'
            project_request.save()
            return redirect('client_portal')  # Redirect to the same page after submitting the form
    else:
        form = ProjectRequestForm()

    pending_projects = ProjectRequest.objects.filter(user=request.user, status='Requested')  # Get projects with status 'Requested'
    active_projects = ProjectRequest.objects.filter(user=request.user, status='In Progress')  # Get projects with status 'In Progress'
    completed_projects = ProjectRequest.objects.filter(user=request.user, status='Completed')  # Get projects with status 'Completed'

    message_form = MessageForm(request.POST or None)
    if request.method == 'POST' and 'content' in request.POST:
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.user = request.user
            message.save()
            return redirect('client_portal')

    return render(request, 'Portal/client_portal.html', {
        'form': form,
        'message_form': message_form,
        'pending_projects': pending_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'user': request.user
    })


def is_admin(user):
    return user.is_superuser  # Ensure only admins can access this view



@login_required
@user_passes_test(is_admin)
def admin_portal(request):
    project_requests = ProjectRequest.objects.all()
    messages = Message.objects.all().order_by('-timestamp')

    # Group messages by user
    messages_by_user = {}
    for message in messages:
        if message.user not in messages_by_user:
            messages_by_user[message.user] = []
        messages_by_user[message.user].append(message)

    return render(request, 'Portal/admin_portal.html', {
        'project_requests': project_requests,
        'messages_by_user': messages_by_user,
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




# Portal/views.py

from .forms import MilestoneForm


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
            form = MilestoneForm(request.POST)
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


@user_passes_test(is_admin)
def accept_request(request, request_id):
    project_request = get_object_or_404(ProjectRequest, id=request_id)
    project_request.status = 'In Progress'
    project_request.save()
    return redirect('admin_portal')


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
        form = MilestoneForm(request.POST, instance=milestone)
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



@login_required
def reply_message(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        content = request.POST.get('reply_content')
        if content:
            Message.objects.create(user=user, content=content)
    return redirect('admin_portal')

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