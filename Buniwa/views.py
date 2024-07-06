from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from .forms import *
import os
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash




# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user = request.user
        user_details, created = UserDetails.objects.get_or_create(user=user)
    logos = theCompany.objects.all()
    return render(request, 'Buniwa/index.html', {'logos': logos})

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('password1')

        if pass1!=pass2:
            return render(request, 'Buniwa/register', {'error': 'Passwords dont match'})
        else:
            my_user=User.objects.create_user(username=uname, email=email, password=pass1, first_name=first_name, last_name=last_name)
            my_user.save()
            return redirect('signin')

    return render(request, 'Buniwa/register.html')

def signin(request):        
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        
        user=authenticate(request, username=username, email=email, password=pass1)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return redirect('signin')
    return render(request, 'Buniwa/signin.html')

def about(request):
    return render(request, 'Buniwa/about.html')

def team(request):
    cards = theTeam.objects.all()
    return render(request, 'Buniwa/team.html', {'cards': cards})

def services(request):
    service_items = theServices.objects.all()
    return render(request, 'Buniwa/services.html', {'service_items':service_items})

def career(request):
    return render(request, 'Buniwa/career.html')

# @login_required(login_url="signin")
def projects(request):
    return render(request, "Buniwa/projects.html")

def faqs(request):
    accordion_items = theFaqs.objects.all()
    return render(request, "Buniwa/faqs.html", {'accordion_items':accordion_items})


def blog(request):
    cards = theBlog.objects.all()
    return render(request, "Buniwa/blog.html", {'cards': cards})

def submit_text(request):
    if request.method == 'POST':
        form = TexTEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('submit_text')
    else:
        form = TexTEntryForm()

    text_entries = TextEntry.objects.all()#retrieve all the entries in the TextEntry Model
    return render(request, 'Buniwa/submit_text.html', {'form': form, 'text_entries': text_entries})

def blog_details(request, pk):
    card = get_object_or_404(theBlog, pk=pk)
    if request.method == 'POST':
        form = blogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user#set the user to the currently logged in user
            comment.post = card#associate the comment with the current blog post
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = blogComment.objects.get(id=parent_id)
                comment.parent = parent_comment
            comment.save() #save the comment to the database
            return redirect('blog_details', pk=pk)
    else:
        form = blogCommentForm()
    blog_comments = blogComment.objects.filter(post=card, parent__isnull=True)
    total_comments = blog_comments.count()
    return render(request, "Buniwa/blog_details.html", {
    # return render(request, "Buniwa/tester.html", {
        'card': card,
        'blog_comments': blog_comments,
        'form': form,
        'total_comments': total_comments
        })

@login_required
def profile(request):
    user = request.user
    user_details, created = UserDetails.objects.get_or_create(user=user)
    profile_photo_url = user_details.profile_photo.url if user_details.profile_photo else 'https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg'

    if request.method == 'POST':
        # Check for profile photo upload or removal
        if 'profile_photo' in request.FILES:
            if user_details.profile_photo:
                if os.path.isfile(user_details.profile_photo.path):
                    os.remove(user_details.profile_photo.path)
            user_details.profile_photo = request.FILES['profile_photo']
            user_details.save()
            messages.success(request, 'Profile photo updated successfully.')
            return redirect('profile')

        elif 'remove_photo' in request.POST:
            if user_details.profile_photo:
                if os.path.isfile(user_details.profile_photo.path):
                    os.remove(user_details.profile_photo.path)
                user_details.profile_photo = None
                user_details.save()
            messages.success(request, 'Profile photo removed successfully.')
            return redirect('profile')

        # Handle profile update
        else:
            form = ProfileForm(request.POST, request.FILES, instance=user_details)
            if form.is_valid():
                form.save()
                user.first_name = request.POST.get('first_name', user.first_name)
                user.last_name = request.POST.get('last_name', user.last_name)
                user.save()
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('profile')
            else:
                print("Profile form errors:", form.errors)
    else:
        form = ProfileForm(instance=user_details)

    return render(request, 'Buniwa/profile.html', {
        'user': user,
        'user_details': user_details,
        'profile_photo_url': profile_photo_url,
        'form': form
    })



def user_logout(request):#User Logs out
    logout(request)
    return redirect('index')

def portfolio(request):
    cards = PortfolioPost.objects.all()
    return render(request, 'Buniwa/portfolio.html', {'cards': cards})

def portfolio_details(request, pk):
    card = get_object_or_404(PortfolioPost, pk=pk)
    return render(request, 'Buniwa/portfolio_details.html', {'card':card})


def testimonial(request):
    testimonial_items = theTestimonials.objects.all()
    return render(request, 'Buniwa/testimonial.html', {'testimonial_items':testimonial_items})

def terms(request):
    return render(request, 'Buniwa/terms.html')

def contact(request):
    return render(request, 'Buniwa/contact.html')
    