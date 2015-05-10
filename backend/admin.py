from django.contrib import admin
from .models import *

class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 1

class TournamentAdmin(admin.ModelAdmin):
    inlines = (ParticipationInline,)

# class PlayerAdmin(admin.ModelAdmin):
#     inlines = (ParticipationInline,)

admin.site.register(Player)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Participation)
admin.site.register(Round)
admin.site.register(Game)
admin.site.register(Award)
admin.site.register(Avatar)