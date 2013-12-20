from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from match.forms import MatchForm, CommentForm
from django.db.models import Q
from match.models import Match, Comment, Club
from django.contrib.auth.models import User
from match.email import *
import thread
import json
import time
from datetime import datetime

def index(request):
  place = ''
  competitor = ''
  start_time = ''
  end_time = ''
  fromdate = ''
  playername = ''
  is_search = False
  # search with place, competitor, player, date
  if 'place' in request.GET:
    place = request.GET['place']
  if 'competitor' in request.GET:
    competitor = request.GET['competitor']
  if 'fromdate' in request.GET:
    fromdate = request.GET['fromdate']
    string = str(request.GET['fromdate']).split('-')
    # convert time to datetimefield model
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(string[0][:-1],'%B %d, %Y'))
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(string[1][1:],'%B %d, %Y'))
  if 'start_time' in request.GET:
    start_time = request.GET['start_time']
  if 'end_time' in request.GET:
    end_time = request.GET['end_time']

  if 'playername' in request.GET:
    playername = request.GET['playername']
  if start_time and end_time:
    if not playername:
      matchs = Match.objects.filter(Q(place__contains=place) & Q(competitor__contains=competitor) & Q(time__gte=start_time, time__lte=end_time))
    else:
      matchs = Match.objects.filter(Q(place__contains=place) & Q(competitor__contains=competitor) & Q(time__gte=start_time, time__lte=end_time) & (Q(player__first_name__contains=playername) | Q(player__last_name__contains=playername))).distinct()
    is_search = True
  else:
    matchs = Match.objects.all()

  club = Club.objects.all()[0]

  # pagination
  paginator = Paginator(matchs,3)
  page = request.GET.get('page')
  try:
    matchs = paginator.page(page)
  except PageNotAnInteger:
    matchs = paginator.page(1)
  except EmptyPage:
    matchs = paginator.page(paginator.num_pages)

  return render(request, 'match/index.html', {'matchs' : matchs, 'club' : club, 'place': place, 'competitor': competitor, 'fromdate': fromdate, 'is_search': is_search, 'playername': playername})

# create a match
@login_required
@permission_required('match.can_modify')
def add(request):
  if request.method == 'POST':
    match = MatchForm(request.POST)
    if match.is_valid():
      new_match = match.save(commit=False)
      new_match.creator = request.user
      new_match.save()
      return HttpResponseRedirect(reverse('match:detail', args=[new_match.id]))
  else:
    match = MatchForm()

  return render(request, 'match/match_form.html', {'match_form' : match}, )

# edit a match
@login_required
@permission_required('match.can_modify')
def edit(request, match_id):
  match_obj = get_object_or_404(Match, pk=match_id)
  if request.method == 'POST' and match_obj:
    match = MatchForm(request.POST)
    if match.is_valid():
      match_obj = match.save(commit=False)
      match_obj.creator = request.user
      match_obj.id = match_id
      match_obj.save()
      return HttpResponseRedirect(reverse('match:detail', args=(match_obj.id,)))
  else:
    match = MatchForm(instance=match_obj)
  return render (request, 'match/match_form.html', {'match_form' : match, 'form_type' : 'edit', })

# delete a match
@login_required
@permission_required('match.can_modify')
def delete(request, match_id):
  match_obj = get_object_or_404(Match, pk=match_id)
  match_obj.delete()
  if 'is_ajax' in request.GET:
    return HttpResponse('success')
  else:
    return HttpResponseRedirect(reverse('match:index'))

# show detail a match
def detail(request, match_id):
  commentform = CommentForm()
  all_player = User.objects.filter(groups__name='player')
  match = get_object_or_404(Match, pk=match_id)
  has_player = change_list(match.player.all())
  is_modify = False
  if request.user.has_perm('match.can_modify'):
    is_modify = True
  else:
    all_player = match.player.all()
  if request.method == 'POST':
    if 'is_comment' in request.POST:
      comment = CommentForm(request.POST)
      if comment.is_valid():
        new_comment = comment.save(commit=False)
        new_comment.match = match
        new_comment.creator = request.user
        new_comment.save()

        return HttpResponseRedirect(reverse('match:detail', args=(match.id,)))

    if 'is_delete_comment' in request.POST and 'comment_id[]' in request.POST:
      comment_list = request.POST.getlist('comment_id[]')
      Comment.objects.filter(pk__in=comment_list).delete()

  context = {
    'has_player' : has_player,
    'all_player' : all_player,
    'match' : match,
    'is_modify' : is_modify,
    'is_join' : request.user in match.player.all(),
    'commentform' : commentform
  }
  return render(request,"match/detail.html", context)

# add player to match
def add_player(request, match_id):
  if request.method == 'POST':
    match = get_object_or_404(Match, pk=match_id)
    user = User.objects.get(pk=request.POST['user_id'])
    if user and match:
      match.player.add(user)
      thread.start_new_thread(send_join_remind_email, (user, match, ))
      response = []
      response_user = {}
      response_user['id'] = user.id
      response_user['username'] = user.username
      response_user['first_name'] = user.first_name
      response_user['last_name'] = user.last_name
      response_user['email'] = user.email
      response_user['pos'] = user.profile.pos
      response_user['num'] = user.profile.num
      response_user['contact'] = user.profile.contact
      response_user['avatar'] = str(user.profile.avatar)
      print user.profile.avatar
      response.append(response_user)
      return HttpResponse(json.dumps(response), content_type="application/json")
  return HttpResponse("failed")

# remove player from a match
def remove_player(request, match_id):
  if request.method == 'POST':
    match = get_object_or_404(Match, pk=match_id)
    user = User.objects.get(pk=request.POST['user_id'])
    if user and match:
      match.player.remove(user)
      thread.start_new_thread(send_unjoin_remind_email, (user, match, ))
      if None != request.POST['reason']:
        comment = Comment()
        comment.match_id = match_id
        comment.reason = request.POST['reason']
        comment.creator = request.user
        comment.save()
        # send reason to manager
        manager = User.objects.filter(groups__name='manager')
        for m in manager:
          thread.start_new_thread(send_reason_unjoin_email, (user, match, request.POST['reason'], m))
      return HttpResponse(comment.id)
  return HttpResponse("failed")

# show matches on calendar
def calendar(request):
  # create match from calendar
  if request.method == 'POST':
    match = Match()
    match.name = request.POST['name']
    #convert time to correct format
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(request.POST['time'],'%m/%d/%Y'))
    match.time = ts
    match.place = request.POST['place']
    match.competitor = request.POST['competitor']
    match.creator = request.user
    match.save()
    #return render(request, "match/calendar.html", )
    return HttpResponse(match.id);
  else:
    return render(request, "match/calendar.html", )

# get match via ajax to show matches on calendar
def get_match(request):
  start = request.GET['start']
  end = request.GET['end']
  start_time = datetime.fromtimestamp(int(start))
  end_time = datetime.fromtimestamp(int(end))
  matchs = Match.objects.filter(Q(time__gte=start_time, time__lte=end_time)| Q(time__lt=start_time))
  response = []

  for match in matchs:
    match_item = {}
    match_item['id'] = match.id
    match_item['editable'] = True
    match_item['title'] = match.name
    match_item['start'] = match.time.isoformat()
    match_item['url'] = reverse('match:detail', args=(match.id,))
    match_item['allDay'] = False

    response.append(match_item)
  return HttpResponse(json.dumps(response), content_type="application/json")

def change_list(obj):
  result = ""
  for x in obj:
    result += str(x.id) + ','
  return result


