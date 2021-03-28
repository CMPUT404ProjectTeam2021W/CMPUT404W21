from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import send_friend_request, accept_friend_request

urlpatterns = [
  path('', views.index, name='index'),
  path('signup/', views.SignUpView.as_view(), name='signup'),
  path('', include('django.contrib.auth.urls')),
  path('image_upload', views.image_view, name = 'image_upload'),
  path('success', views.success, name = 'success'),
  path('feed/', views.feed, name='feed'),
  path('create_post/', views.create_post, name='create_post'),
  path('', include('django.contrib.auth.urls')),
  path('profile/', views.profile_posts, name='profile'),
  path('user_settings/', views.user_settings, name = 'user_settings'),

  path('author/<str:author_id>/', views.author_profile, name='author_profile'),

  path('send_friend_request/<str:author_id>/', send_friend_request, name='send friend request'),
  path('accept_friend_request/<str:request_id>/', accept_friend_request, name='accept friend request'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
