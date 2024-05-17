from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
 path('', views.home, name='home'),
  path('accounts/', include('django.contrib.auth.urls')),
  path('login/',auth_views.LoginView.as_view(template_name='templates/login.html'), name = 'login'),
  path('logout/',auth_views.LogoutView.as_view(template_name='templates/logout.html'), name = 'logout'),
  path('newpost/', views.managepost, name='managepost'),
  path('newinternship/', views.manageinternship, name='manageinternship'),
  path('posts/', views.posts, name='posts'),
  path('post/<int:pk>/edit/', views.PostUpdate.as_view(), name='post_edit'),
  path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
  path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
]