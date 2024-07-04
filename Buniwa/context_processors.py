from .models import UserDetails

def profile_photo(request):
    if request.user.is_authenticated:
        user_details = UserDetails.objects.get(user=request.user)
        profile_photo_url = user_details.profile_photo.url if user_details.profile_photo else 'https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg'
        return {'profile_photo_url': profile_photo_url}
    return {}
