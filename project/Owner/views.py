from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
# Create your views here.




@login_required
def owner(request):
    # Fetch all users
    mem = User.objects.all()

    # Pass the logged-in user's details to the context
    context = {
        'mem': mem,
        'username': request.user.username,  # Get the logged-in user's username
        'email': request.user.email,        # Get the logged-in user's email
    }

    return render(request, 'owner/owner.html', context)