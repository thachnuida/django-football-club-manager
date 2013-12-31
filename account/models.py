from django.db import models
from django.contrib.auth.models import User

TITLE_CHOICES = (
	('GK', 'GK'),
	('CB', 'CB'),
  ('LB', 'LB'),
  ('RB', 'RB'),
  ('DM', 'DM'),
  ('LWB', 'LWB'),
  ('RWB', 'RWB'),
  ('RM', 'RM'),
  ('CM', 'CM'),
  ('RF', 'RF'),
  ('CF', 'CF'),
  ('LF', 'LF'),
  ('RAM', 'RAM'),
  ('CAM', 'CAM'),
  ('LAM', 'LAM'),
	)

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	pos = models.CharField(max_length=50, choices=TITLE_CHOICES, blank=True)
	num = models.IntegerField(max_length=100,blank=True, null=True, )
	avatar = models.ImageField(upload_to="img", blank=True, default='defaultUserAvatar.jpg')
	contact = models.CharField(max_length=50, blank=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
