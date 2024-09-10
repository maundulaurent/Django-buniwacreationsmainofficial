from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name = 'register'),
    path('signin', views.signin, name = 'signin'),
    path('about', views.about, name = 'about'),
    path('team', views.team, name = 'team'),
    path('services', views.services, name = 'services'),
    # --------- services pages  -------------------#

    path('web-development', views.web_dev, name = 'web_development'),
    path('seo', views.seo, name = 'seo'),
    path('social-marketing', views.social_marketing, name = 'social_marketing'),
    path('content-creation', views.content_creation, name = 'content_creation'),
    path('paid-advertising', views.paid_advertising, name = 'paid_advertising'),
    path('audio-video-production', views.audio_video, name = 'audio_video'),
    path('location-based-marketing', views.location_based, name = 'location_based'),
    

    # --------- services pages  -------------------#
    path('career', views.career, name = 'career'),
    path('contact', views.contact, name = 'contact'),
    path('portal', views.portal, name="portal"),
    path('faqs', views.faqs, name="faqs"),
    path('blog', views.blog, name="blog"),
    path('blog/<int:pk>/', views.blog_details, name="blog_details"),
    path('profile',views.profile, name="profile"),
    path('logout',views.user_logout, name='logout'),
    path('portfolio',views.portfolio, name="portfolio"),
    path('portfolio/<int:pk>/',views.portfolio_details, name="portfolio_details"),
    path('testimonial',views.testimonial, name="testimonial"),
    path('terms',views.terms, name="terms"),
    path('blog/<int:pk>/',views.blog_details, name="tester"),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
