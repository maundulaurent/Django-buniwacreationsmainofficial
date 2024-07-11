# Portal/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import ProjectRequest
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required

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

@login_required
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


def is_admin(user):
    return user.is_superuser  # Ensure only admins can access this view

@user_passes_test(is_admin)
def accept_request(request, request_id):
    project_request = get_object_or_404(ProjectRequest, id=request_id)
    project_request.status = 'In Progress'
    project_request.save()
    return redirect('admin_portal')

# Portal/views.py

from .forms import MilestoneForm

@user_passes_test(is_admin)
def create_milestones(request, request_id):
    project_request = get_object_or_404(ProjectRequest, id=request_id)
    if request.method == 'POST':
        form = MilestoneForm(request.POST)
        if form.is_valid():
            # Handle the form submission, save milestones related to the project
            # Here you need to implement the actual milestone creation logic
            # For example:
            # Milestone.objects.create(
            #     project_request=project_request,
            #     title=form.cleaned_data['title'],
            #     description=form.cleaned_data['description'],
            #     due_date=form.cleaned_data['due_date']
            # )
            return redirect('admin_portal')
    else:
        form = MilestoneForm()

    return render(request, 'Portal/create_milestones.html', {'form': form})


@user_passes_test(is_admin)
def complete_project(request, request_id):
    project_request = get_object_or_404(ProjectRequest, id=request_id)
    project_request.status = 'Completed'
    project_request.save()
    return redirect('admin_portal')

@login_required
def reply_message(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        content = request.POST.get('reply_content')
        if content:
            Message.objects.create(user=user, content=content)
    return redirect('admin_portal')