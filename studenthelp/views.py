from .models import Transport
from django.contrib import messages  
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import HousingForm, InternshipForm, PostForm, RecommendationForm, TransportForm
from .models import Housing, Internship, Post, Like, Comment, Recommendation
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from .forms import EventForm

def home(request):
    posts = Post.objects.all()
    return render(request, 'studenthelp/home.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Welcome {username}, your account has been created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Post, Like

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Post, Like



@login_required
def like_post(request):
    if request.method == 'POST':

        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        

        existing_like = Like.objects.filter(user=request.user, post=post).first()
        if existing_like:
            existing_like.delete()
            liked = False
        else:

            like = Like(user=request.user, post=post)
            like.save()
            liked = True
        response_data = {
            'liked': liked,
            'like_count': post.likes.count()  
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(response_data)
        else:
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return redirect('home', pk=post_id)



@login_required
def add_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        post = get_object_or_404(Post, pk=post_id)
        Comment.objects.create(post=post, user=request.user, content=content)
    return redirect('home')

@login_required
def managepost(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.save()
            messages.success(request, 'New Post created successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Failed to create the Post.')
    else:
        form = PostForm(initial={'creator': request.user})  
    return render(request, 'studenthelp/newpost.html', {'form': form})


def posts(request):
    posts = Post.objects.all()
    return render(request, 'studenthelp/ListPosts.html', {'posts': posts})
  

class PostDelete(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'studenthelp/post_confirm_delete.html'
    success_url = reverse_lazy('home')


class PostDetail(LoginRequiredMixin,DetailView):
    template_name = 'studenthelp/post_detail.html'
    model = Post
    

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'studenthelp/edit_post.html'  # Assuming you have a template for editing posts
    fields = "__all__"  # Or specify the fields you want to include in the form
    success_url = reverse_lazy('home')  # Assuming you have a URL named 'post_detail'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs.get('pk'))
      
def internships(request):
    internships = Internship.objects.all()
    return render(request, 'studenthelp/listInternships.html', {'internships': internships})    
class InternshipDelete(LoginRequiredMixin, DeleteView):
    model = Internship
    template_name = 'studenthelp/delete_intership.html'
    success_url = reverse_lazy('home')

class InternshipDetail(LoginRequiredMixin, DetailView):
    template_name = 'studenthelp/details_internship.html'
    model = Internship

class InternshipUpdate(LoginRequiredMixin, UpdateView):
    model = Internship
    template_name = 'studenthelp/edit_internship.html'
    fields = "__all__"
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return get_object_or_404(Internship, pk=self.kwargs.get('pk'))

from django.contrib import messages

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import InternshipForm

@login_required
def manageinternship(request):
    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.creator = request.user
            internship.save()
            messages.success(request, 'New Internship created successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Failed to create the Internship. Please correct the errors below.')
    else:
        form = InternshipForm(initial={'creator': request.user}) 
    return render(request, 'studenthelp/newinternship.html', {'form': form})


def list_transports(request):
    transports = Transport.objects.all()
    return render(request, 'studenthelp/list_transports.html', {'transports': transports})

@login_required
def create_transport(request):
    if request.method == 'POST':
        form = TransportForm(request.POST)
        if form.is_valid():
            transport = form.save(commit=False)
            transport.creator = request.user
            transport.save()
            messages.success(request, 'Transport created successfully.')
            return redirect('home')
    else:
        form = TransportForm()
    return render(request, 'studenthelp/transport_form.html', {'form': form})

@login_required
def update_transport(request, pk):
    transport = get_object_or_404(Transport, pk=pk)
    if request.method == 'POST':
        form = TransportForm(request.POST, instance=transport)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transport updated successfully.')
            return redirect('studenthelp/list_transports')
    else:
        form = TransportForm(instance=transport)
    return render(request, 'studenthelp/transport_form.html', {'form': form})

@login_required
def delete_transport(request, pk):
    transport = get_object_or_404(Transport, pk=pk)
    if request.method == 'POST':
        transport.delete()
        messages.success(request, 'Transport deleted successfully.')
        return redirect('home')
    return render(request, 'studenthelp/delete_transport.html', {'transport': transport})




def list_events(request):
    events = Event.objects.all()
    return render(request, 'studenthelp/list_events.html', {'events': events})

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'studenthelp/event_form.html', {'form': form})

def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EventForm(instance=event)
    return render(request, 'studenthelp/event_form.html', {'form': form})

def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('home')
    return render(request, 'studenthelp/delete_event.html', {'event': event})


def list_housing(request):
    housings = Housing.objects.all()
    return render(request, 'studenthelp/list_housing.html', {'housings': housings})

@login_required
def create_housing(request):
    if request.method == 'POST':
        form = HousingForm(request.POST)
        if form.is_valid():
            housing = form.save(commit=False)
            housing.creator = request.user  # Make sure your model has a creator field if using this
            housing.save()
            print("Housing created successfully")
            return redirect(reverse_lazy('home'))
        else:
            print("Form is not valid")
    else:
        form = HousingForm()
    return render(request, 'studenthelp/housing_form.html', {'form': form})

@login_required
def edit_housing(request, pk):
    housing = get_object_or_404(Housing, pk=pk)
    if request.method == 'POST':
        form = HousingForm(request.POST, instance=housing)
        if form.is_valid():
            form.save()
            print("Housing edited successfully")
            return redirect(reverse_lazy('home'))
        else:
            print("Form is not valid")
    else:
        form = HousingForm(instance=housing)
    return render(request, 'studenthelp/housing_form.html', {'form': form})
def delete_housing(request, pk):
    housing = get_object_or_404(Housing, pk=pk)
    if request.method == 'POST':
        housing.delete()
        return redirect('home')
    return render(request, 'studenthelp/delete_housing.html', {'housing': housing})

def list_recommendations(request):
    recommendations = Recommendation.objects.all()
    return render(request, 'studenthelp/list_recommendations.html', {'recommendations': recommendations})

def create_recommendation(request):
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            recommendation = form.save(commit=False)
            recommendation.creator = request.user
            recommendation.save()
            return redirect('home')
    else:
        form = RecommendationForm()
    return render(request, 'studenthelp/recommendation_form.html', {'form': form})

def edit_recommendation(request, pk):
    recommendation = get_object_or_404(Recommendation, pk=pk)
    if request.method == 'POST':
        form = RecommendationForm(request.POST, instance=recommendation)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RecommendationForm(instance=recommendation)
    return render(request, 'studenthelp/recommendation_form.html', {'form': form})

def delete_recommendation(request, pk):
    recommendation = get_object_or_404(Recommendation, pk=pk)
    if request.method == 'POST':
        recommendation.delete()
        return redirect('home')
    return render(request, 'studenthelp/delete_recommendation.html', {'recommendation': recommendation})
