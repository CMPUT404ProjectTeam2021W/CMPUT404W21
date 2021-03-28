from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'authors', views.AuthorViewSet)


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
  path('/api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
