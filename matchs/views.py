# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    return HttpResponse("Hi, you are in matchs index.")

def detail(request, match_id):
    return render_to_response('matchs/detail.html', {'match_id': match_id}) # this view is using Template.

def add(request, match_id):
    return render_to_response('matchs/form.html', {'match_id': match_id})

def edit(request, match_id):
    return render_to_response('matchs/form.html', {'match_id': match_id})

def delete(request, match_id):
    return HttpResponse("I deleted the match %s." % match_id)