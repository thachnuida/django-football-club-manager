from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from accounts.models import FacebookSession
from django.conf import settings
import urllib2
import json
import cgi
import urllib

# login with social accounts
def login(request, provider):
  if 'next' in request.GET:
    redirect_url = request.GET['next']
    error_message = ''
  else:
    redirect_url = '/match/'
    error_message = ''
  error = None
  if request.user.is_authenticated():
    return HttpResponseRedirect('/match/')

  if request.GET:
    #sign in with facebook
    if provider == 'fb':
      if 'code' in request.GET:
        args = {
          'client_id': settings.FACEBOOK_APP_ID,
          'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
          'client_secret': settings.FACEBOOK_API_SECRET,
          'code': request.GET['code'],
        }
        url = 'https://graph.facebook.com/oauth/access_token?' + \
              urllib.urlencode(args)
        response = cgi.parse_qs(urllib.urlopen(url).read())
        access_token = response['access_token'][0]
        expires = response['expires'][0]
        facebook_session = FacebookSession.objects.get_or_create(access_token=access_token)[0]
        facebook_session.expires = expires
        facebook_session.save()
        user = auth.authenticate(token=access_token, type=provider)
        if user:
          if user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(redirect_url)
          else:
            error = 'AUTH_DISABLED'
        else:
          error = 'AUTH_FAILED'
      elif 'error_reason' in request.GET:
        error = 'AUTH_DENIED'
    # sign in with github
    if provider == 'github':
      if 'code' in request.GET:
        args = {
          'client_id': settings.GITHUB_APP_ID,
          'client_secret': settings.GITHUB_API_SECRET,
          'code': request.GET['code'],
          'redirect_uri': settings.GITHUB_REDIRECT_URI,
        }
        url = 'https://github.com/login/oauth/access_token?' + urllib.urlencode(args)
        print url
        headers = {'Accept': 'application/json'}
        req = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(req).read()
        result  = json.loads(response)
        access_token = result['access_token']
        facebook_session = FacebookSession.objects.get_or_create(
          access_token=access_token
        )[0]
        facebook_session.save()
        user = auth.authenticate(token=access_token, type=provider)
        if user:
          if user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(redirect_url)
          else:
            error = 'AUTH_DISABLED'
        else:
          error = 'AUTH_FAILED'
      elif 'error_reason' in request.GET:
        error = 'AUTH_DENIED'
  template_context = {'settings': settings, 'error': error, 'response': response}
  return render_to_response('account/login.html', template_context, context_instance=RequestContext(request))