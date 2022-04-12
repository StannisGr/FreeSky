from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.SingInView.as_view(), name='sign_in'),
    path('signup/', views.SingUpView.as_view(), name='sign_up'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('logout', views.get_sing_up),
]
