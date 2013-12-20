from django.db import models
from django.contrib.auth.models import User

class Match(models.Model):
  name = models.CharField(max_length=100)
  time = models.DateTimeField(null=True, blank=True)
  place = models.CharField(max_length=200, blank=True)
  competitor = models.CharField(max_length=100, blank=True)
  result = models.CharField(max_length=100, null=True, blank=True)
  player = models.ManyToManyField(User, related_name='player', null=True, blank=True)
  creator = models.ForeignKey(User, blank=True, null=True)

  class Meta:
      ordering = ['-time']
      permissions = (
        ("can_modify", "Can modify match add,edit,delete"),
        ("can_joinmatch","Player can join match"),
      )
  def __unicode__(self):
      return self.name

class Club(models.Model):
  photo = models.ImageField(upload_to='img', blank=True)
  name = models.CharField(max_length=100,blank=True, null=True)
  address = models.CharField(max_length=200,null=True, blank=True)

class Comment(models.Model):
  creator = models.ForeignKey(User, blank=True, null=True)
  comment = models.TextField(max_length=400, blank=True, null=True)
  created = models.DateTimeField(auto_now_add=True)
  reason = models.TextField(max_length=400, blank=True, null=True)
  match = models.ForeignKey(Match)

