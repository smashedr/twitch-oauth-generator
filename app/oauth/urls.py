from django.urls import path, re_path

import oauth.views as views

app_name = 'oauth'


urlpatterns = [
    path('code/', views.do_oauth, name='code'),
    path('token/', views.do_oauth, name='token'),
    path('logout/', views.log_out, name='logout'),
    path('callback/', views.callback, name='callback'),
]
