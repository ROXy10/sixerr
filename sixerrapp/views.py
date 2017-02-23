from django.shortcuts import render, redirect
from .models import Gig


def home(request):
    gigs = Gig.objects.filter(status=True)
    context = {
        'gigs': gigs,
    }
    return render(request, 'home.html', context)


def gig_detail(request, id):
    try:
        gig = Gig.objects.get(id=id)
    except Gig.DoesNotExist:
        return redirect('/')

    context = {
        'gig': gig,
    }
    return render(request, 'gig_detail.html', context)