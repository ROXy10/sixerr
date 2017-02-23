from django.shortcuts import render
from .models import Gig


def home(request):
    gigs = Gig.objects.filter(status=True)
    context = {
        'gigs': gigs,
    }
    return render(request, 'home.html', context)


def gig_detail(request, id):
    return render(request, 'gig_detail.html', {})