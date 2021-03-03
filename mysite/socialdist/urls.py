from django.urls import path, include

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('signup', views.SignUpView.as_view(), name='signup'),
  # path('login',views.LogInView.as_view(), name='login'),
  path('', include('django.contrib.auth.urls'))

]
