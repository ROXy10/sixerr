from django.conf.urls import url
from sixerrapp.views import home, gig_detail, create_gig, my_gigs

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^gigs/(?P<id>[0-9]+)/$', gig_detail, name='gig_detail'),
    url(r'^my_gigs/$', home, name='my_gigs'),
    url(r'^create_gig/$', home, name='create_gig'),
]