from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import theClient, theAdmin, ProjectRequest, Milestone, ChatMessage
from .forms import ProjectRequestForm, MilestoneForm, ChatMessageForm

SINGLE_CLIENT_ID = 1  # Update this ID to match the ID of your demo client in the database

def client_portal(request):
    try:
        client = theClient.objects.get(id=SINGLE_CLIENT_ID)
    except theClient.DoesNotExist:
        return render(request, 'Portal/error_page.html', {'message': 'Client does not exist'})

    requests = ProjectRequest.objects.filter(client=client)
    active_projects = requests.filter(status='Approved')
    completed_projects = requests.filter(status='Completed')
    pending_projects = requests.filter(status='Pending')

    if request.method == 'POST':
        form = ProjectRequestForm(request.POST)
        if form.is_valid():
            project_request = form.save(commit=False)
            project_request.client = client
            project_request.save()
            return redirect('client_portal')
    else:
        form = ProjectRequestForm()

    return render(request, 'Portal/client_portal.html', {
        'requests': requests,
        'form': form,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'pending_projects': pending_projects,
    })

def admin_portal(request):
    requests = ProjectRequest.objects.all()
    return render(request, 'Portal/admin_portal.html', {'requests': requests})

def approve_request(request, request_id):
    project_request = get_object_or_404(ProjectRequest, id=request_id)
    project_request.status = 'Approved'
    project_request.save()
    return redirect('admin_portal')

def add_milestone(request, request_id):
    project_request = get_object_or_404(ProjectRequest, id=request_id)
    if request.method == 'POST':
        form = MilestoneForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.project_request = project_request
            milestone.save()
            return redirect('admin_portal')
    else:
        form = MilestoneForm()
    return render(request, 'Portal/add_milestone.html', {'form': form, 'project_request': project_request})

def view_project_details(request, request_id):
    project_request = get_object_or_404(ProjectRequest, id=request_id)
    milestones = Milestone.objects.filter(project_request=project_request)
    messages = ChatMessage.objects.filter(project_request=project_request).order_by('timestamp')
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.project_request = project_request
            chat_message.sender = request.user
            chat_message.save()
            return redirect('view_project_details', request_id=request_id)
    else:
        form = ChatMessageForm()
    return render(request, 'Portal/project_details.html', {
        'project_request': project_request,
        'milestones': milestones,
        'messages': messages,
        'form': form,
    })

def complete_project(request, request_id):
    project_request = get_object_or_404(ProjectRequest, id=request_id)
    project_request.status = 'Completed'
    project_request.save()
    return redirect('admin_portal')

def chat(request):
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.sender = request.user
            chat_message.save()
            return redirect('chat')
    else:
        form = ChatMessageForm()
    
    messages = ChatMessage.objects.all().order_by('timestamp')
    return render(request, 'Portal/chat.html', {
        'form': form,
        'messages': messages
    })