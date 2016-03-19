# -*- coding: utf-8 -*-
from __future__ import division
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import glob
from myproject.myapp.models import Document
from myproject.myapp.models import Response, UserDetails
from myproject.myapp.forms import DocumentForm
import subprocess
from subprocess import Popen, PIPE
import os.path

script_dir = "myproject/myapp/"
directory = "myproject/media/documents/";

def runScript():
    # print "ayaya"
    subprocess.call(directory + "Clean.sh",shell=True)
    # print "runn"
    # print paperid
    file_name = glob.glob(directory+'*.pdf')
    # print file_name
    srno = 1
    fname = file_name[0]
    fn = fname.split('/')
    fn = fn[-1]
    print fn
    # subprocess.call("clear", shell=True)
    subprocess.call("mv " + directory + fn + " " + directory + "input.pdf", shell=True)
    subprocess.call(directory + "IntegratedShellScript.sh ", shell=True)

    return HttpResponse("Done")

def list(request):
    if request.method == 'GET':
        return HttpResponseRedirect("/home/")
        # return HttpResponse('This page shows a list of most recent posts.')
        # pass
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            runScript()

            # Redirect to the document list after POST
            return HttpResponseRedirect("/home/")
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'myapp/home.html',
        {'documents': documents, 'form': form},

        context_instance=RequestContext(request)
    )

def author_names(request):
    return render(request, "myapp/author_names.html")

def title(request):
    return render(request, "myapp/title.html")

def home(request):
    return render(request, "myapp/home.html")

def email(request):
    return render(request, "myapp/email.html")

def affiliation(request):
    return render(request, "myapp/affiliation.html")

def map(request):
    return render(request, "myapp/map.html")

def section(request):
    return render(request, "myapp/section.html")

def table_heading(request):
    return render(request, "myapp/table_heading.html")

def figure_heading(request):
    return render(request, "myapp/figure_heading.html")

def getauthor(request):
    if request.method == 'GET':
        resp = ""
        if os.path.isfile(directory + "eval_author.txt"):
            resp = open(directory + "eval_author.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/author_names/'}
        return HttpResponse(resp, content_type='string')

def gettitle(request):
    if request.method == 'GET':
        resp = ""
        if os.path.isfile(directory + "eval_title.txt"):
            resp = open(directory + "eval_title.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/title/'}
        return HttpResponse(resp, content_type='string')

def getemail(request):
    if request.method == 'GET':
        resp = ""
        if os.path.isfile(directory + "eval_emails.txt"):
            resp = open(directory + "eval_emails.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/email/'}
        return HttpResponse(resp, content_type='string')

def getaffiliation(request):
    if request.method == 'GET':
        resp = ""
        if os.path.isfile(directory + "eval_Affiliations.txt"):
            resp = open(directory + "eval_Affiliations.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/affiliation/'}
        return HttpResponse(resp, content_type='string')

def getmap(request):
    if request.method == 'GET':
        resp = ""
        if os.path.isfile(directory + "eval_map.txt"):
            resp = open(directory + "eval_map.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/map/'}
        return HttpResponse(resp, content_type='string')

def getsection(request):
    if request.method == 'GET':
        resp = ""
        if os.path.isfile(directory + "eval_Secmap.txt"):
            resp = open(directory + "eval_Secmap.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/section/'}
        return HttpResponse(resp, content_type='string')

def gettabfig(request):
    if request.method == 'GET':
        resp = ""
        if os.path.isfile(directory + "eval_tables_figures.txt"):
            resp = open(directory + "eval_tables_figures.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/table_heading/'}
        return HttpResponse(resp, content_type='string')
