from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views.authenticationviews import *
from .views.authorviews import *
from .views.postviews import *

from  .api.apiviews import *


urlpatterns = [
  path('', index, name='index'),
  path('signup/', SignUpView.as_view(), name='signup'),
  path('',  include('django.contrib.auth.urls')),
  # path('image_upload', image_view, name='image_upload'),
  # path('success', success, name='success'),

  path('',  include('django.contrib.auth.urls')),
  path('user_settings/', user_settings, name = 'user_settings'),
  # post urls here
  path('feed/', feed, name='feed'),
  path('create_post/', create_post, name='create_post'),
  path('posts/<str:post_id>/view_post/', view_post, name='view_post'),
  path('posts/<str:post_id>/delete/', delete_post, name='delete_post'),
  path('like/<str:post_id>/', like, name='like'),
  path('unlike/<str:post_id>/', unlike, name='unlike'),
  path('share/<str:post_id>/', share, name='share'),
  path('unshare/<str:post_id>/', unshare, name='unshare'),
  path('unlisted/', unlisted_posts, name='unlisted_posts'),

  # author profile urls here
  path('author/<str:author_id>/', author_profile, name='author_profile'),
  path('author/<str:author_id>/followers/', followers, name='followers'),
  path('author/<str:author_id>/', author_profile, name='author_profile'),
  path('follow/<str:author_id>/', follow, name='follow'),
  path('unfollow/<str:author_id>/', unfollow, name='unfollow'),


  # ------------------------------ api urls here --------------------------------------------
  path("api/authors/", AuthorList.as_view(), name='author_list'),
  path("api/posts/", PostList.as_view(), name='post_list'),
  path("api/author/<uuid:author_id>/posts/<uuid:post_id>", PostDetails.as_view(), name='post_detail'),
  path("api/author/<uuid:author_id>/", AuthorDetails.as_view(), name='author_detail'),
  path("api/author/<uuid:author_id>/followers/", FollowerList.as_view(), name='followers_list'),
  path("api/author/<uuid:author_id>/followers/<uuid:foreign_author_id>", FollowerAction.as_view(), name='followers_action'),
  path("/author/<uuid:author_id>/posts/<uuid:post_id>/comments", CommentsList.as_view(), name='comments_list'),
  path("api/author/<uuid:author_id>/friends/", FriendsList.as_view(), name='friends_list'),
   ## path("api/author/<uuid:author_id>/posts/<uuid:post_id>/", CommentsList.as_view(), name='comments_list'),
   ## path("api/author/<uuid:author_id>/liked", LikedList.as_view(), name='liked_list'),


]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
