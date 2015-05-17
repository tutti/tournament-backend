from django.db import models
from xml.etree import ElementTree
from django.contrib.auth.models import User
import base64
import hashlib
from datetime import datetime
from django import forms

class Player(models.Model):
    POINTS_1ST = 10
    POINTS_2ND = 5
    POINTS_3RD = 3
    POINTS_4TH = 2
    MAXTOURNAMENTS = 6
    TOPTOURNAMENTS = 4

    name = models.CharField(max_length=255)
    pop_id = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=1, default='M')
    visible = models.BooleanField(default=True)
    max_score = models.IntegerField(default=0)
    awards = models.ManyToManyField('Award', blank=True)
    avatar = models.ForeignKey('Avatar')
    default_password = models.CharField(max_length=10)
    
    def __str__(self):
        return str(self.pop_id) + " " + self.name

    def add_award(self, award_name):
        self.awards.add(Award.objects.get(name=award_name))
        self.save()

    def calculate_recent_score(self):
        tournaments = Tournament.objects.all()[:self.MAXTOURNAMENTS]
        participations = []
        for tournament in tournaments:
            participation = tournament.participation_set.filter(player=self).first()
            if participation is not None:
                participations.append(participation)
        scores = []
        for participation in participations:
            if participation.placement == 1:
                scores.append(self.POINTS_1ST)
            elif participation.placement == 2:
                scores.append(self.POINTS_2ND)
            elif participation.placement == 3:
                scores.append(self.POINTS_3RD)
            elif participation.placement == 4:
                scores.append(self.POINTS_4TH)

        score = sum(sorted(scores, key=lambda score: -score)[:self.TOPTOURNAMENTS])

        if score > self.max_score:
            self.max_score = score
            self.save()

        return score

    def count_outcomes(self, outcome):
        participations = Participation.objects.filter(player=self)
        if (outcome == 0):
            return len(participations)
        count = 0
        for participation in participations:
            if participation.placement == outcome:
                count += 1
        return count

    def update_awards(self):
        # Updates awards for:
        #   - Participation
        #   - 1 and 10 wins, 2nds and 3rds
        #   - Staffing
        #   - 20 and 30 score
        participates = self.count_outcomes(0)
        firsts = self.count_outcomes(1)
        seconds = self.count_outcomes(2) + firsts
        thirds = self.count_outcomes(3) + seconds
        staff = len(self.tournament_staff.all())
        score = self.calculate_recent_score()
        if participates >= 1:
            self.add_award("Pokéball")
        if participates >= 5:
            self.add_award("Great Ball")
        if participates >= 10:
            self.add_award("Ultra Ball")
        if participates >= 50:
            self.add_award("Master Ball")
        if firsts >= 1:
            self.add_award("Nugget")
        if firsts >= 10:
            self.add_award("Big Nugget")
        if seconds >= 1:
            self.add_award("Pearl")
        if seconds >= 10:
            self.add_award("Big Pearl")
        if thirds >= 1:
            self.add_award("Stardust")
        if thirds >= 10:
            self.add_award("Star Piece")
        if staff >= 1:
            self.add_award("Cherish Ball")
        if score >= 20:
            self.add_award("Luxury Ball")
        if score >= 30:
            self.add_award("Premier Ball")

    def get_eligible_avatars(self):
        avatars = []
        avatarObjects = Avatar.objects.all()
        for obj in avatarObjects:
            if self.is_eligible_avatar(obj):
                avatars.append(obj)
        return avatars

    def is_eligible_avatar(self, avatar):
        if avatar.name_male == "School Kid":
            return True
        firsts = self.count_outcomes(1)
        staff = len(self.tournament_staff.all())
        if avatar.name_male == "Rich Boy" and firsts >= 1:
            return True
        if avatar.name_male == "Blackbelt" and firsts >= 5:
            return True
        if avatar.name_male == "Psychic" and firsts >= 10:
            return True
        if avatar.name_male == "Ace Trainer" and firsts >= 25:
            return True
        if avatar.name_male == "Champion" and staff >= 1:
            return True
        if avatar.name_male == "Gym Leader" and self.max_score >= 40:
            return True
        return False

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(default=datetime.now)
    players = models.ManyToManyField(Player, through='Participation', related_name='tournament_players', blank=True)
    staff = models.ManyToManyField(Player, related_name='tournament_staff', blank=True)
    xml = models.TextField()
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-date"]

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

        # Get the organiser's user object
        organiser_id = data.find("organizer").attrib["popid"]
        organiser_name = data.find("organizer").attrib["name"]
        organiser, created = Player.objects.get_or_create(pop_id=organiser_id, defaults=player_defaults)
        # There will be no default password, and the name will not be set.
        # The intended case is for the organiser to already have an account.
        # Add the staff award to the organiser, and the organiser to the staff.
        organiser.add_award("Cherish Ball")
        tournament.staff.add(organiser)

        # Get the date
        dateRaw = data.find("startdate").text
        date = datetime.strptime(dateRaw, "%m/%d/%Y")
        tournament.date = date

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
            players[pop_id] = { 'player': player, 'pop_id': pop_id, 'wins': 0, 'losses': 0, 'ties': 0, 'matches': 0, 'bye': False, 'score': 0, 'owp': 0, 'oowp': 0, 'opponents': [] }

        # Create the round and game objects
        roundElements = root.find("pods").find("pod").find("rounds").findall("round")
        for element in roundElements:
            # Create the round object
            roundnum = element.attrib['number']
            round = Round.objects.create(roundnum=roundnum, tournament=tournament)

            matchElements = element.find("matches").findall("match")

            for melem in matchElements:
                # Create each game object
                outcome = int(melem.attrib['outcome'])
                if outcome == 5:
                    # This was a bye match
                    p1id = melem.find("player").attrib['userid']
                    p2id = False
                    player1 = players[p1id]['player']
                    player2 = False
                    game = Game.objects.create(round=round, player1=player1, player2=None, winner=5)

                    players[p1id]['matches'] += 1
                    players[p1id]['wins'] += 1
                    players[p1id]['bye'] = True
                elif outcome == 8:
                    # The player was late, and not present for this round
                    p1id = melem.find("player").attrib['userid']
                    p2id = False
                    player1 = players[p1id]['player']
                    player2 = False
                    game = Game.objects.create(round=round, player1=player1, player2=None, winner=8)

                    players[p1id]['matches'] += 1
                    players[p1id]['losses'] += 1
                else:
                    p1id = melem.find("player1").attrib['userid']
                    p2id = melem.find("player2").attrib['userid']
                    player1 = players[p1id]['player']
                    player2 = players[p2id]['player']
                    game = Game.objects.create(round=round, player1=player1, player2=player2, winner=outcome)

                    # Update the wins and losses of both players
                    players[p1id]['opponents'].append(p2id)
                    players[p2id]['opponents'].append(p1id)
                    players[p1id]['matches'] += 1
                    players[p2id]['matches'] += 1
                    if outcome == 1:
                        players[p1id]['wins'] += 1
                        players[p2id]['losses'] += 1
                    elif outcome == 2:
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
                this_opponent_wins = players[oid]['wins']
                this_opponent_ties = players[oid]['ties']
                this_opponent_matches = players[oid]['matches']
                # If a player got a bye, disregard that player's bye match
                # (subtract 1 from wins and matches).
                if (players[oid]['bye']):
                    this_opponent_wins -= 1
                    this_opponent_matches -= 1
                opwin = 100 * (2*this_opponent_wins + this_opponent_ties) / (2*this_opponent_matches)
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

            if pid not in dnf:
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

        # Add the dropped award to players who didn't finish
        for did in dnf:
            players[did]['player'].add_award("Escape Rope")

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
    player2 = models.ForeignKey(Player, related_name='game_p2', null=True, blank=True)
    winner = models.SmallIntegerField() # 1 or 2 for player 1 or 2, 3 for tie, 5 for bye, 8 for late
    
    def __str__(self):
        return str(self.round) + ": " + str(self.player1) + " vs " + str(self.player2)

    def get_winner(self):
        if self.winner == 1:
            return self.player1
        if self.winner == 2:
            return self.player2
        return None

    def winner_name(self):
        if self.winner == 1:
            return self.player1.name
        if self.winner == 2:
            return self.player2.name
        if self.winner == 3:
            return "Uavgjort"
        if self.winner == 5:
            return "Bye"

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

    class Meta:
        ordering = ["placement"]

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