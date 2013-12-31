from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from account.forms import UserForm, UserProfileForm, RegisterForm
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.conf import settings

def index(request):
  return render(request, 'index.html')

#login with user & password
def site_login(request):
  error_message = "Login user is required !"
  if 'next' in request.GET:
    redirect_url = request.GET['next']
    error_message = ''
  else:
    redirect_url = '/match/'
    error_message = ''

  if request.POST:
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        return redirect(redirect_url)
      else:
        error_message = "User is not active"
    else:
      error_message = "Invalid user or password"
  return render(request, 'account/login.html',{
				"error_message": error_message,
        "settings": settings,
				})

# update or show user profile
@login_required
def profile(request):
  profile = request.user.profile
  if request.POST:
    user_form = UserForm(request.POST, instance=request.user)
    user_profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
    if user_form.is_valid() and user_profile_form.is_valid():
      user_form.save()
      user_profile_form.save()
  else:
    user_form = UserForm(instance=request.user)
    user_profile_form = UserProfileForm(instance=profile)
  context = {
    'user_form': user_form,
    'user_profile_form': user_profile_form,
    'profile': profile
  }
  return render(request, 'account/profile.html', context)

# register player via manager
@login_required
def register(request):
 # user_form = UserCreationForm()
  user_form = RegisterForm()
  user_profile_form = UserProfileForm()
  if request.POST:
    user_form = RegisterForm(request.POST)
    if user_form.is_valid():
      u = user_form.save()
      g = Group.objects.get(name='player')
      g.user_set.add(u)
      profile = u.profile
      user_profile_form = UserProfileForm(request.POST, instance=profile)
      user_profile_form.save()
      return HttpResponseRedirect(reverse('account:register'))

  context = {
    'user_form': user_form,
    'user_profile_form': user_profile_form,
  }
  return render(request, 'account/register.html', context)

# update or show user profile
@login_required
@permission_required('match.can_modify')
def edit(request, user_id):
  user = get_object_or_404(User, pk=user_id)
  profile = user.profile
  if request.POST:
    user_form = UserForm(request.POST, instance=user)
    user_profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
    if user_form.is_valid() and user_profile_form.is_valid():
      user_form.save()
      user_profile_form.save()
  else:
    user_form = UserForm(instance=user)
    user_profile_form = UserProfileForm(instance=profile)
  context = {
    'user_form': user_form,
    'user_profile_form': user_profile_form,
    'profile': profile
  }
  return render(request, 'account/profile.html', context)

# delete player
@login_required
@permission_required('match.can_modify')
def delete(request, user_id):
  user = get_object_or_404(User, pk=user_id)
  user.delete()
  return HttpResponseRedirect(reverse('account:list_player'))

# show list player
@login_required
@permission_required('match.can_modify')
def list_player(request):
  is_modify = False
  if request.user.has_perm('match.can_modify'):
    is_modify = True
  lp = User.objects.filter(groups__name='player')
  context = {
    'is_modify' : is_modify,
    'list_player' : lp,
  }
  return render(request, 'account/list_player.html', context)

# logout
def site_logout(request):
  logout(request)
  return redirect('/account/login')
