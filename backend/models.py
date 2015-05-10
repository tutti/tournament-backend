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

    def add_award(self, award_id):
        self.awards.add(Award.objects.get(pk=award_id))

    def count_outcomes(self, outcome):
        participations = Participation.objects.filter(player=self)
        count = 0
        if (outcome == 0):
            return len(participations)
        for participation in participations:
            if participation.placement == outcome:
                count += 1
        return count

    def update_awards(self):
        participates = self.count_outcomes(0)
        firsts = self.count_outcomes(1)
        seconds = self.count_outcomes(2) + firsts
        thirds = self.count_outcomes(3) + seconds
        print(str(participates) + " " + str(firsts) + " " + str(seconds) + " " + str(thirds))
        if participates >= 1:
            self.add_award(1)
        if participates >= 5:
            self.add_award(2)
        if participates >= 10:
            self.add_award(3)
        if participates >= 50:
            self.add_award(4)
        if firsts >= 1:
            self.add_award(5)
        if firsts >= 10:
            self.add_award(6)
        if seconds >= 1:
            self.add_award(7)
        if seconds >= 10:
            self.add_award(8)
        if thirds >= 1:
            self.add_award(9)
        if thirds >= 10:
            self.add_award(10)

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

        # Start at the root
        root = ElementTree.fromstring(xml)

        # Read basic data about the tournament
        data = root.find("data")
        tournament = Tournament.objects.create(xml=xml, name=data.find("name").text)

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

            matchElements = element.find("matches").findall("match")

            for melem in matchElements:
                # Create each game object
                p1id = melem.find("player1").attrib['userid']
                p2id = melem.find("player2").attrib['userid']
                player1 = players[p1id]['player']
                player2 = players[p2id]['player']
                game = Game.objects.create(round=round, player1=player1, player2=player2, winner=melem.attrib['outcome'])

                # Update the wins and losses of both players
                players[p1id]['opponents'].append(p2id)
                players[p2id]['opponents'].append(p1id)
                players[p1id]['matches'] += 1
                players[p2id]['matches'] += 1
                if int(melem.attrib['outcome']) == 1:
                    players[p1id]['wins'] += 1
                    players[p2id]['losses'] += 1
                elif int(melem.attrib['outcome']) == 2:
                    players[p1id]['losses'] += 1
                    players[p2id]['wins'] += 1
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

        # Update all participants' awards
        for i in range(len(sorted_players)):
            sorted_players[i]['player'].update_awards()

        # Return the tournament
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