from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect

from .models import *

def index(request):
    players = sorted(Player.objects.all(), key=lambda player: -player.calculate_recent_score())
    current_position = 0
    current_score = 100
    for counter, player in enumerate(players):
        score = player.calculate_recent_score()
        if score < current_score:
            current_position = counter
            current_score = score
        player.position = current_position + 1
    context = { 'players': players }

    if len(Tournament.objects.all()) >= 6:
        for player in players:
            if player.position == 1:
                player.add_award("Relic Crown")
            if player.position <= 2:
                player.add_award("Relic Statue")
            if player.position <= 3:
                player.add_award("Relic Vase")

    return render(request, 'backend/index.html', context)

def view_player(request, pop_id):
    player = Player.objects.get(pop_id=pop_id)

    player.update_awards()

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
        Tournament.from_xml(contents)
    return render(request, 'backend/upload_tournament.html', context)

@login_required
def change_password(request):
    context = { 'errors': [] }
    if request.method == 'POST':
        oldpass = request.POST['oldpass']
        newpass1 = request.POST['newpass1']
        newpass2 = request.POST['newpass2']
        checkuser = authenticate(username=request.user.username, password=oldpass)
        if checkuser is None:
            context['errors'].append("Feil passord.")
        if newpass1 != newpass2:
            context['errors'].append("Fyll inn samme passord i begge feltene for nytt passord.")
        if len(context['errors']) > 0:
            return render(request, 'backend/change_password.html', context)
        checkuser.set_password(newpass1)
        checkuser.save()
        logout(request)
        return render(request, 'backend/change_password_success.html', context)
    return render(request, 'backend/change_password.html', context)

@login_required
def choose_avatar(request):
    player = Player.objects.get(pop_id=request.user.username)
    context = {}
    if request.method == 'POST':
        avatar = Avatar.objects.get(pk=request.POST['avatar'])
        if player.is_eligible_avatar(avatar):
            player.avatar = avatar
            player.save()
            context['messages'] = [
                "Avataren din har blitt endret."
            ]
        else:
            context['errors'] = [
                "Ugyldig avatarvalg."
            ]
    context['gender'] = player.gender
    context['avatars'] = player.get_eligible_avatars()
    context['selected'] = player.avatar
    return render(request, 'backend/choose_avatar.html', context)

def tournaments(request):
    tournaments = Tournament.objects.all()
    context = { 'tournaments': tournaments, 'title': "Alle turneringer" }
    return render(request, 'backend/tournament_list.html', context)

@login_required
def player_tournaments(request, pop_id):
    player = Player.objects.get(pop_id=pop_id)
    tournaments = player.tournament_players.all()
    context = { 'tournaments': tournaments, 'title': "Turneringer for " + player.name }
    return render(request, 'backend/tournament_list.html', context)

def view_tournament(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    context = { 'tournament': tournament }
    return render(request, 'backend/view_tournament.html', context)