from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from . import views
from  .api.apiviews import *


urlpatterns = [
  path('', views.index, name='index'),
  path('signup/', views.SignUpView.as_view(), name='signup'),
  path('', include('django.contrib.auth.urls')),
  path('image_upload', views.image_view, name='image_upload'),
  path('success', views.success, name='success'),
  path('feed/', views.feed, name='feed'),
  path('create_post/', views.create_post, name='create_post'),
  path('', include('django.contrib.auth.urls')),
  path('user_settings/', views.user_settings, name = 'user_settings'),
  path('posts/<str:post_id>/view_post/', views.view_post, name='view_post'),
  path('posts/<str:post_id>/delete/', views.delete_post, name='delete_post'),
  path('author/<str:author_id>/', views.author_profile, name='author_profile'),
  path('author/<str:author_id>/followers/', views.followers, name='followers'),
  path('author/<str:author_id>/', views.author_profile, name='author_profile'),
  path("api/authors/", AuthorList.as_view(), name='author_list'),
  path("api/posts/", PostList.as_view(), name='post_list'),
  path("api/author/<uuid:author_id>/", AuthorDetails.as_view(), name='author_detail'),
  path("api/author/<uuid:author_id>/followers/", FollowerList.as_view(), name='followers_list'),
  path("api/author/<uuid:author_id>/followers/<uuid:foreign_author_id>", FollowerAction.as_view(), name='followers_action'),
  path("api/author/<uuid:author_id>/friends/", FriendsList.as_view(), name='friends_list'),
  ## path("api/author/<uuid:author_id>/posts/<uuid:post_id>/", CommentsList.as_view(), name='comments_list'),
  ## path("api/author/<uuid:author_id>/liked", LikedList.as_view(), name='liked_list'),

  path('follow/<str:author_id>/', views.follow, name='follow'),
  path('unfollow/<str:author_id>/', views.unfollow, name='unfollow'),

  path('like/<str:post_id>/', views.like, name='like'),
  path('unlike/<str:post_id>/', views.unlike, name='unlike'),
  path('share/<str:post_id>/', views.share, name='share'),
  path('unshare/<str:post_id>/', views.unshare, name='unshare'),

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
