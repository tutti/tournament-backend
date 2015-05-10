from django.db import models
from xml.etree import ElementTree
from django.contrib.auth.models import User
import base64
import hashlib

class Player(models.Model):
    name = models.CharField(max_length=255)
    pop_id = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=1, default='M')
    visible = models.BooleanField(default=True)
    awards = models.ManyToManyField('Award', blank=True)
    avatar = models.ForeignKey('Avatar')
    default_password = models.CharField(max_length=10)
    
    def __str__(self):
        return str(self.pop_id) + " " + self.name

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    players = models.ManyToManyField(Player, through='Participation', related_name='tournament_players', blank=True)
    staff = models.ManyToManyField(Player, related_name='tournament_staff', blank=True)
    xml = models.TextField()
    
    def __str__(self):
        return self.name

    @staticmethod
    def from_xml(xml):
        # Default values for creating player objects
        player_defaults = {
            'avatar': Avatar.objects.get(id=1),
            'visible': True,
            'gender': 'M'
        }

        # Create a tournament object
        # tournament.xml = xml

        # Start at the root
        root = ElementTree.fromstring(xml)

        # Read basic data about the tournament
        data = root.find("data")
        tournament = Tournament.objects.create(xml=xml, name=data.find("name").text)
        # tournament.name = data.find("name").text
        # tournament.save()

        # Create player (and user) objects for players who do not have them yet
        playerElements = root.find("players").findall("player")
        players = {}
        for element in playerElements:
            pop_id = element.attrib['userid']

            # Get a player object
            player, created = Player.objects.get_or_create(pop_id=pop_id, defaults=player_defaults)

            # If that object was newly created, set the player's name and create a user
            if created:
                # Create a default password
                line = u'n4LraIKuXnsdRHqpaG4P' + pop_id
                hasher = hashlib.md5(line.encode('utf-8'))
                default_pass = base64.urlsafe_b64encode(hasher.digest())[0:10]

                # Update the player's name, add the default password, and save.
                player.name = element.find("firstname").text + " " + element.find("lastname").text
                player.default_password = default_pass
                player.save()

                # Create the user
                user = User.objects.create_user(pop_id, '', default_pass)
            players[pop_id] = { 'player': player, 'pop_id': pop_id, 'wins': 0, 'losses': 0, 'ties': 0, 'matches': 0, 'score': 0, 'owp': 0, 'oowp': 0, 'opponents': [] }

        # Create the round and game objects
        roundElements = root.find("pods").find("pod").find("rounds").findall("round")
        for element in roundElements:
            # Create the round object
            roundnum = element.attrib['number']
            round = Round.objects.create(roundnum=roundnum, tournament=tournament)
            # round.roundnum = roundnum
            # round.tournament = tournament
            # round.save()

            matchElements = element.find("matches").findall("match")

            for melem in matchElements:
                # Create each game object
                p1id = melem.find("player1").attrib['userid']
                p2id = melem.find("player2").attrib['userid']
                player1 = players[p1id]['player']
                player2 = players[p2id]['player']
                game = Game.objects.create(round=round, player1=player1, player2=player2, winner=melem.attrib['outcome'])
                # game.round = round
                # game.player1 = player1
                # game.player2 = player2
                # game.winner = melem.attrib['outcome']
                # game.save()

                # Update the wins and losses of both players
                players[p1id]['opponents'].append(p2id)
                players[p2id]['opponents'].append(p1id)
                players[p1id]['matches'] += 1
                players[p2id]['matches'] += 1
                if int(melem.attrib['outcome']) == 1:
                    players[p1id]['wins'] += 1
                    players[p2id]['losses'] += 1
                    print("winner 1")
                elif int(melem.attrib['outcome']) == 2:
                    players[p1id]['losses'] += 1
                    players[p2id]['wins'] += 1
                    print("winner 2")
                else:
                    players[p1id]['ties'] += 1
                    players[p2id]['ties'] += 1

        # Figure out which players did not finish
        dnf = {}
        for podelem in root.find("standings").findall("pod"):
            if podelem.attrib['type'] == 'dnf':
                for playerelem in podelem.findall("player"):
                    dnf[playerelem.attrib['id']] = True

        sorted_players = [] # To be a sorted list of POP IDs

        # Calculate positioning and tiebreaker scores
        for pid in players:
            pinfo = players[pid]
            # Calculate score
            pinfo['score'] = 3*pinfo['wins'] + pinfo['ties']

            # Calculate opponents' win from each opponent's win percentage
            opponent_wins = 0
            for oid in pinfo['opponents']:
                opwin = 100*(players[oid]['wins'] / players[oid]['matches'])
                # opwin = players[oid]['wins']
                if opwin < 25:
                    opwin = 25
                if oid in dnf and opwin > 75:
                    opwin = 75
                opponent_wins += opwin
            pinfo['owp'] = opponent_wins / len(pinfo['opponents']);

        for pid in players:
            pinfo = players[pid]
            # Calculate opponents' opponents' win from each opponent's owp
            opponent_opwins = 0
            for oid in pinfo['opponents']:
                opponent_opwins += players[oid]['owp']
            pinfo['oowp'] = opponent_opwins / len(pinfo['opponents']);

            sorted_players.append(pinfo)

        # Sort the players list
        sorted_players.sort(key=lambda player: -player['oowp'])
        sorted_players.sort(key=lambda player: -player['owp'])
        sorted_players.sort(key=lambda player: -player['score'])

        for i in range(len(sorted_players)):
            pinfo = sorted_players[i]
            participation = Participation.objects.create(
                tournament=tournament,
                placement=i+1,
                player=pinfo['player'],
                wins=pinfo['wins'],
                losses=pinfo['losses'],
                ties=pinfo['ties'],
                owp=pinfo['owp'],
                oowp=pinfo['oowp']
            )
        tournament.save()
        return tournament

class Round(models.Model):
    tournament = models.ForeignKey(Tournament)
    roundnum = models.IntegerField()
    
    def __str__(self):
        return str(self.tournament) + " round " + str(self.roundnum)

class Game(models.Model):
    round = models.ForeignKey(Round)
    player1 = models.ForeignKey(Player, related_name='game_p1')
    player2 = models.ForeignKey(Player, related_name='game_p2')
    winner = models.SmallIntegerField() # 1 or 2 for player 1 or 2, 3 for tie
    
    def __str__(self):
        return str(self.round) + ": " + str(self.player1) + " vs " + str(self.player2)

class Participation(models.Model):
    tournament = models.ForeignKey(Tournament)
    player = models.ForeignKey(Player)
    placement = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    ties = models.IntegerField()
    owp = models.DecimalField(max_digits=5, decimal_places=2)
    oowp = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return str(self.tournament) + ": " + str(self.player)

class Award(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField()
    
    def __str__(self):
        return self.name + ": " + self.description

class Avatar(models.Model):
    name_male = models.CharField(max_length=255)
    name_female = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image_male = models.ImageField()
    image_female = models.ImageField()
    
    def __str__(self):
        if self.name_male == self.name_female:
            return self.name_male
        return self.name_male + " / " + self.name_female