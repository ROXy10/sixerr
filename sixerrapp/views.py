from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

import braintree

from .models import Gig, Profile, Purchase, Review
from .forms import GigForm


braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id='8ykhmn7wsdn2xqm7',
                                  public_key='43t9nrz7gk33r482',
                                  private_key='b9ae0d74068c14ef1ba6a073ad5dd5cb')


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

    if request.user.is_anonymous():
        show_post_review = False
    else:
        show_post_review = Purchase.objects.filter(gig=gig, buyer=request.user).count() > 0

    reviews = Review.objects.filter(gig=gig)

    client_token = braintree.ClientToken.generate()
    context = {
        'show_post_review' : show_post_review,
        'reviews': reviews,
        'client_token': client_token,
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


@login_required(login_url="/")
def create_purchase(request):
    if request.method == 'POST':
        try:
            gig = Gig.objects.get(id=request.POST['gig_id'])
        except Gig.DoesNotExist:
            return redirect('/')

        nonce = request.POST["payment_method_nonce"]
        result = braintree.Transaction.sale({
            "amount": gig.price,
            "payment_method_nonce": nonce
        })

        if result.is_success:
            Purchase.objects.create(gig=gig, buyer=request.user)
    return redirect('/')


@login_required(login_url="/")
def my_sellings(request):
    purchases = Purchase.objects.filter(gig__user=request.user)

    context = {
        'purchases': purchases,
    }
    return render(request, 'my_sellings.html', context)


@login_required(login_url="/")
def my_buyings(request):
    purchases = Purchase.objects.filter(buyer=request.user)

    context = {
        'purchases': purchases,
    }
    return render(request, 'my_buyings.html', context)