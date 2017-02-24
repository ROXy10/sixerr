from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Gig, Profile
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
    error = ''
    if request.method == 'POST':
        gig_form = GigForm(request.POST, request.FILES)
        if gig_form.is_valid():
            gig = gig_form.save(commit=False)
            gig.user = request.user
            gig.save()
            return redirect('my_gigs')
        else:
            error = 'Data is not valid'

    gig_form = GigForm()
    context = {
        'gig_form': gig_form,
        'error': error,
    }
    return render(request, 'create_gig.html', context)


@login_required(login_url='/')
def edit_gig(request, id):
    try:
        gig = Gig.objects.get(id=id, user=request.user)
        error = ''
        if request.method == 'POST':
            gig_form = GigForm(request.POST, request.FILES, instance=gig)
            if gig_form.is_valid():
                gig.save()
                return redirect('my_gigs')
            else:
                error = 'Data is not valid'
        context = {
            'gig': gig,
            'error': error,
        }
        return render(request, 'edit_gig.html', context)
    except Gig.DoesNotExist:
        return redirect('/')


@login_required(login_url='/')
def my_gigs(request):
    gigs = Gig.objects.filter(user=request.user)

    context = {
        'gigs': gigs
    }
    return render(request, 'my_gigs.html', context)


@login_required(login_url='/')
def profile(request, username):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        profile.about = request.POST['about']
        profile.slogan = request.POST['slogan']
        profile.save()
    else:
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return redirect('/')

    gigs = Gig.objects.filter(user=profile.user, status=True)
    context = {
        'profile': profile,
        'gigs': gigs,
    }
    return render(request, 'profile.html', context)