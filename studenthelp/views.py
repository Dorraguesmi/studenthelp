from django.contrib import messages  
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import InternshipForm, PostForm
from .models import Post


from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "studenthelp/home.html")

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
  
@login_required
def manageinternship(request):
    if request.method == 'POST':
        form = InternshipForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, 'New Post created successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Failed to create the Post.')
    return render(request, 'studenthelp/internshipform.html', {'form': form})


def posts(request):
    posts = Post.objects.all()
    return render(request, 'studenthelp/ListPosts.html', {'posts': posts})

  
class PostDelete(DeleteView):
    model = Post
    template_name = 'studenthelp/post_confirm_delete.html'
    success_url = reverse_lazy('posts')

class PostDetail(DetailView):
    template_name = 'studenthelp/post_detail.html'
    model = Post
    
class PostUpdate(UpdateView):
    model = Post
    template_name = 'studenthelp/newpost.html'
    fields = "__all__"
    success_url = reverse_lazy('posts')
