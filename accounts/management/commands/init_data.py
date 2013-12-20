__author__ = 'quocnguyen'
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from match.models import Club
class Command(BaseCommand):
  def handle(self, *args, **options):
    player = Group.objects.get_or_create(name='player')
    manager = Group.objects.get_or_create(name='manager')
    match_permission = Permission.objects.get_or_create(codename='can_modify')
    player_permission = Permission.objects.get_or_create(codename='can_joinmatch')
    manager.permissions = [match_permission]
    player.permissions = [player_permission]
    # Create club name
    Club.objects.get_or_create(name='HTK-FC')
