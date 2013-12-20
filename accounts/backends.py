from django.contrib.auth import models as auth_models
from accounts import models
import urllib
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify

class FacebookBackend:
  # authenticate user via social accounts
  def authenticate(self, token=None, type=None):
    user = {}
    if type == 'fb':
      facebook_session = models.FacebookSession.objects.get(
          access_token=token,
      )
      profile = facebook_session.query('me',type=type)
      try:
          user = auth_models.User.objects.get(username=profile['id'])
      except auth_models.User.DoesNotExist, e:
          user = auth_models.User(username=profile['id'])

      user.set_unusable_password()
      user.email = profile['email']
      user.first_name = profile['first_name']
      user.last_name = profile['last_name']
      user.save()

      url = "http://graph.facebook.com/%s/picture?type=large" % profile["id"]
      avatar = urllib.urlopen(url)
      user.profile.avatar.save(slugify(user.username + " social") + '.jpg', ContentFile(avatar.read()))

      try:
        models.FacebookSession.objects.get(uid=profile['id']).delete()
      except models.FacebookSession.DoesNotExist, e:
        pass

      facebook_session.uid = profile['id']
      facebook_session.user = user
      facebook_session.save()

    if type == 'github':
      facebook_session = models.FacebookSession.objects.get(
          access_token=token,
      )
      profile = facebook_session.query(type=type)
      try:
        user = auth_models.User.objects.get(username=profile['id'])
      except auth_models.User.DoesNotExist, e:
        user = auth_models.User(username=profile['id'])
      url = profile['avatar_url']
      url += '&s=200'
      avatar = urllib.urlopen(url)
      user.profile.avatar.save(slugify(user.username + " github") + '.jpg',
                                ContentFile(avatar.read()))
      user.set_unusable_password()
      user.first_name = profile['login']
      user.save()

      try:
        models.FacebookSession.objects.get(uid=profile['id']).delete()
      except models.FacebookSession.DoesNotExist, e:
        pass
      facebook_session.uid = profile['id']
      facebook_session.user = user
      facebook_session.save()

    return user

  def get_user(self, user_id):
    try:
      return auth_models.User.objects.get(pk=user_id)
    except auth_models.User.DoesNotExist:
      return None