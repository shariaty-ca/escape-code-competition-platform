from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Competition, Participant
from .forms import RegistrationForm, CompetitionRegistrationForm
from django.utils import timezone

def home(request):
    """Homepage view showing active competitions"""
    now = timezone.now()
    competitions = Competition.objects.filter(
        is_active=True,
        end_date__gte=now
    ).order_by('start_date')
    
    context = {
        'competitions': competitions,
        'now': now  # Useful for template logic
    }
    return render(request, 'registration/home.html', context)

def user_register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def competition_detail(request, pk):
    """Competition detail and registration view"""
    competition = get_object_or_404(Competition, pk=pk)
    participants_count = Participant.objects.filter(competition=competition).count()
    registered = Participant.objects.filter(
        user=request.user,
        competition=competition
    ).exists()
    
    # Handle registration submission
    if request.method == 'POST' and not registered:
        form = CompetitionRegistrationForm(request.POST, competition=competition)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.user = request.user
            participant.competition = competition
            participant.save()
            messages.success(request, "Successfully registered for the competition!")
            return redirect('competition_detail', pk=pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CompetitionRegistrationForm(competition=competition)
    
    context = {
        'competition': competition,
        'form': form,
        'registered': registered,
        'participants_count': participants_count,
        'spots_remaining': competition.max_participants - participants_count,
        'registration_open': (
            competition.is_active and 
            timezone.now() < competition.end_date and
            participants_count < competition.max_participants
        )
    }
    return render(request, 'registration/competition_detail.html', context)