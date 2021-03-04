from django.urls import path, include

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('signup/', views.SignUpView.as_view(), name='signup'),
  path('feed/', views.feed, name='feed'),
  path('', include('django.contrib.auth.urls'))

]
