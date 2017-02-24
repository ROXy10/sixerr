from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Gig
from .forms import GigForm


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


@login_required(login_url='/')
def create_gig(request):
    if request.method == 'POST':
        gig_form = GigForm(request.POST, request.FILES)
        print(gig_form.is_valid())

    gig_form = GigForm()
    context = {
        'gig_form': gig_form
    }
    return render(request, 'create_gig.html', context)


@login_required(login_url='/')
def my_gigs(request):
    gigs = Gig.objects.filter(user=request.user)

    context = {
        'gigs': gigs
    }
    return render(request, 'my_gigs.html', context)