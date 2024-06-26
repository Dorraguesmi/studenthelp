from django.forms import ModelForm
from .models import Post,Event,Internship,Recommendation,Housing,Comment,Transport
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostForm(ModelForm):
  class Meta :
    model = Post
    fields = ['title', 'description', 'type', 'image'] 
class EventForm(ModelForm):
  class Meta :
    model = Event
    fields = "__all__" 

class InternshipForm(ModelForm):
  class Meta :
    model = Internship
    fields = "__all__" 
    
class RecommendationForm(ModelForm):
  class Meta :
    model = Recommendation
    fields = "__all__" 
    
class HousingForm(ModelForm):
  class Meta :
    model = Housing
    fields = "__all__" 
    
class TransportForm(ModelForm):
  class Meta :
    model = Transport
    fields = "__all__" 
    
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class LikeForm(forms.Form):
    post_id = forms.IntegerField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
