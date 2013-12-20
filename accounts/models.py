from django.db import models
from django.contrib.auth.models import User

class FacebookSessionError(Exception):   
    def __init__(self, error_type, message):
        self.message = message
        self.type = error_type
    def get_message(self): 
        return self.message
    def get_type(self):
        return self.type
    def __unicode__(self):
        return u'%s: "%s"' % (self.type, self.message)
        
class FacebookSession(models.Model):
    access_token = models.CharField(max_length=103, unique=True)
    expires = models.IntegerField(null=True)
    user = models.ForeignKey(User, null=True)
    uid = models.BigIntegerField(unique=True, null=True)
        
    class Meta:
        unique_together = (('user', 'uid'), ('access_token', 'expires'))
        
    def query(self, object_id=None,type=None,connection_type=None, metadata=False):
      response = {}
      import urllib
      import simplejson
      if type == 'fb':
        url = 'https://graph.facebook.com/%s' % (object_id)
        if connection_type:
            url += '/%s' % (connection_type)

        params = {'access_token': self.access_token}
        if metadata:
            params['metadata'] = 1

        url += '?' + urllib.urlencode(params)
        response = simplejson.load(urllib.urlopen(url))
        if 'error' in response:
            error = response['error']
            raise FacebookSessionError(error['type'], error['message'])
      if type == 'github':
        url = 'https://api.github.com/user'
        params  = {'access_token': self.access_token}
        url += '?' + urllib.urlencode(params)
        print "DAY LA URL GITHUB %s " % url
        response = simplejson.load(urllib.urlopen(url))
      return response