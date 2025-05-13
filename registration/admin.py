from django.contrib import admin
from .models import Competition, Participant

class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    inlines = [ParticipantInline]

admin.site.register(Participant)