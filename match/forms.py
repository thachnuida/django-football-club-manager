from match.models import Match, Comment
from django import forms
from django.forms import ModelForm

class MatchForm(ModelForm):
  class Meta:
    model = Match
    fields = ('name', 'time', 'place', 'competitor', 'result')
    widgets = {
      'time': forms.TextInput(attrs={'class':'form-control', 'id':'time'}),
      'name':forms.TextInput(attrs={'class':'form-control', }),
      'place':forms.TextInput(attrs={'class':'form-control', }),
      'competitor':forms.TextInput(attrs={'class':'form-control', }),
      'result':forms.TextInput(attrs={'class':'form-control', }),
    }

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    exclude = ("creator", "created", "reason", "match")
    widgets = {
      'comment': forms.Textarea(attrs={'class':'form-control','rows':'3', 'id':'match_comment'}),
    }