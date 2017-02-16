from django.conf.urls import url
from sixerrapp.views import home, gig_detail

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^gigs/(?P<id>[0-9]+)/$', gig_detail, name='gig_detail'),
]