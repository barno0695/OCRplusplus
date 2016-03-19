# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from myapp import views

urlpatterns = patterns('',
	# (r'^myapp/', include('myproject.myapp.urls')),
    url(r'^author_names/$', views.author_names, name = 'author_names'),
	url(r'^getauthor/$', views.getauthor, name = 'getauthor'),
	url(r'^gettitle/$', views.gettitle, name = 'gettitle'),
	url(r'^title/$', views.title, name = 'title'),
	url(r'^home/$', views.home, name = 'home'),
	url(r'^$', views.home, name = 'home'),
	url(r'^myapp/list/$', views.home, name = 'home'),
	url(r'^email/$', views.email, name = 'email'),
	url(r'^getemail/$', views.getemail, name = 'getemail'),
	url(r'^list/$', views.list, name = 'list'),
    url(r'^affiliation/$', views.affiliation, name = 'affiliation'),
	url(r'^getaffiliation/$', views.getaffiliation, name = 'getaffiliation'),
	url(r'^citation/$', views.citation, name = 'citation'),
    url(r'^reference/$', views.reference, name = 'reference'),
    url(r'^map/$', views.map, name = 'map'),
	url(r'^getmap/$', views.getmap, name = 'getmap'),
    url(r'^url/$', views.url, name = 'url'),
	url(r'^geturl/$', views.geturl, name = 'geturl'),
    url(r'^footnote/$', views.footnote, name = 'footnote'),
	url(r'^getfootnote/$', views.getfootnote, name = 'getfootnote'),
    url(r'^section/$', views.section, name = 'section'),
	url(r'^getsection/$', views.getsection, name = 'getsection'),
    url(r'^table_heading/$', views.table_heading, name = 'table_heading'),
    url(r'^figure_heading/$', views.figure_heading, name = 'figure_heading'),
	url(r'^gettabfig/$', views.gettabfig, name = 'gettabfig'),
    url(r'^getcitref/$', views.getcitref, name = 'getcitref'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
