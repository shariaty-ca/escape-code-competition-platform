from django.db import models
from django.contrib.auth.models import User

class Competition(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_participants = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    team_name = models.CharField(max_length=100, blank=True, null=True)
    # Add any other participant-specific fields
    
    class Meta:
        unique_together = ('user', 'competition')  # Prevent duplicate registrations

    def __str__(self):
        return f"{self.user.username} - {self.competition.name}"