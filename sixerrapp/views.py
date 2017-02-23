from django.shortcuts import render, redirect
from django.views.generic import DetailView
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


def create_gig(request):
    context = {
    }
    return render(request, 'create_gig.html', context)


def my_gigs(request):
    context = {
    }
    return render(request, 'my_gigs.html', context)