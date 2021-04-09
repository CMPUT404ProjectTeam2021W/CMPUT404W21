#from mysite.mysite.settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views.authenticationviews import *
from .views.authorviews import *
from .views.postviews import *
from django.conf.urls import url, include
from markdownx import urls as markdownx

from  .api.apiviews import *


urlpatterns = [
  path('', index, name='index'),
  path('signup/', SignUpView.as_view(), name='signup'),
  path('',  include('django.contrib.auth.urls')),
  # path('image_upload', image_view, name='image_upload'),
  # path('success', success, name='success'),
  #url(r'^markdownx/', include(markdownx)), #see how this works lol
  path('markdownx/', include('markdownx.urls')),
  #static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
  #static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
  path('',  include('django.contrib.auth.urls')),
  path('user_settings/', user_settings, name = 'user_settings'),
  # post urls here
  path('feed/', feed, name='feed'),
  path('friends_feed/', friends_feed, name='friends_feed'),
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
  path('author/<str:author_id>/friends/', friends, name='friends'),
  path('author/<str:author_id>/', author_profile, name='author_profile'),
  path('send_friend_request/<uuid:author_id>/', send_friend_request, name='send_friend_request'),
  path('accept_friend_request/<uuid:request_id>/', accept_friend_request, name='accept_friend_request'),
  path('reject_friend_request/<uuid:request_id>/', reject_friend_request, name='reject_friend_request'),
  path('cancel_friend_request/<uuid:author_id>/', cancel_friend_request, name='cancel_friend_request'),
  path('unfriend/<uuid:author_id>/', unfriend, name='unfriend'),


  # ------------------------------ api urls here --------------------------------------------
  path("api/authors/", AuthorList.as_view(), name='author_list'),
  path("api/posts/", PostList.as_view(), name='post_list'),
  path("api/author/<uuid:author_id>/posts/<uuid:post_id>/", PostDetails.as_view(), name='post_detail'),
  path("api/author/<uuid:author_id>/", AuthorDetails.as_view(), name='author_detail'),
  path("api/author/<uuid:author_id>/followers/", FollowerList.as_view(), name='followers_list'),
  path("api/author/<uuid:author_id>/followers/<uuid:foreign_author_id>/", FollowerAction.as_view(), name='followers_action'),
  path("api/author/<uuid:author_id>/posts/<uuid:post_id>/comments/", CommentsList.as_view(), name='comments_list'),
   ## path("api/author/<uuid:author_id>/posts/<uuid:post_id>/", CommentsList.as_view(), name='comments_list'),
   ## path("api/author/<uuid:author_id>/liked", LikedList.as_view(), name='liked_list'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
