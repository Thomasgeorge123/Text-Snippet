from django.urls import path
from .views import *
from django.urls import re_path
from rest_framework_simplejwt import views as jwt_views
from authentication import views

urlpatterns = [
    re_path('login/',Login.as_view(),name='login'),
    re_path('changepassword/(?P<user_id>[0-9]+)/$',Changepassword.as_view(),name='changepassword'),
    re_path('userregister/',UserRegister.as_view(),name='userregister'),
    re_path('userlist/',UserList.as_view(),name='userlist'),
    re_path('userbyid/(?P<pk>[0-9]+)/$',UserById.as_view(),name='userbyid'),
    re_path('refreshtoken/',jwt_views.TokenRefreshView.as_view(),name ='refreshtoken'),
]




