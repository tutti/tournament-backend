from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect

from .models import *

def index(request):
    context = {}
    return render(request, 'backend/index.html', context)

def view_player(request, pop_id):
    player = Player.objects.get(pop_id=pop_id)
    context = {
        'name': player.name,
        'pop_id': pop_id,
        'firsts': player.count_outcomes(1),
        'seconds': player.count_outcomes(2),
        'thirds': player.count_outcomes(3),
        'participation_count': player.count_outcomes(0),
        'awards': player.awards.all()
    }

    # Add the avatar link
    if player.gender == 'M':
        context['avatar_url'] = player.avatar.image_male.url
    else:
        context['avatar_url'] = player.avatar.image_female.url
    return render(request, 'backend/view_player.html', context)

def login_user(request):
    context = {}
    if request.method == 'POST':
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is None:
            context['errors'] = [
                "Kunne ikke logge inn."
            ]
        else:
            context['username'] = request.POST["username"]
            login(request, user)
            return render(request, "backend/login_success.html", context)
    return render(request, 'backend/login_form.html', context)

def logout_user(request):
    logout(request)
    return redirect('/')

@permission_required('backend.add_tournament', login_url='/login/')
def upload_tournament(request):
    context = {}
    if request.method == 'POST':
        contents = request.FILES['tournamentFile'].read()
        #tournament = Tournament()
        #tournament.xml = contents
        #tournament.save()
        Tournament.from_xml(contents)
    return render(request, 'backend/upload_tournament.html', context)