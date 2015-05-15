from django.contrib import admin
from .models import *

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female")
)

class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 1

class TournamentAdmin(admin.ModelAdmin):
    inlines = (ParticipationInline,)

class PlayerAdminForm(forms.ModelForm):
    class Meta:
        exclude = ['visible']

    def __init__(self, *args, **kwargs):
        super(PlayerAdminForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget = admin.widgets.AdminRadioSelect()
        self.fields['gender'].widget.choices = GENDER_CHOICES
    # class Meta:
    #     fields = {
    #         'name': forms.TextInput,
    #         'gender': forms.Select
    #     }

class PlayerAdmin(admin.ModelAdmin):
    form = PlayerAdminForm
    inlines = (ParticipationInline,)

admin.site.register(Player, PlayerAdmin)
admin.site.register(Tournament, TournamentAdmin)
#admin.site.register(Participation)
admin.site.register(Round)
admin.site.register(Game)
admin.site.register(Award)
admin.site.register(Avatar)