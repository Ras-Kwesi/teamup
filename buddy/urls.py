from django.conf.urls import url
from . import views

urlpatterns=[
    # url('^$',views.index,name='index'),
    # url('^search/',views.search,name='search'),
    url('profile/$', views.profile, name='profile'),
    url('^chatroom/(\w+)', views.chatroom, name='chatroom'),
    url('^gym/(\w+)', views.gym, name='gym'),
    url('^post/(\w+)$', views.post, name='post'),

    url('^update/$', views.update, name='update'),
    url('^newgym/$', views.newgym, name='newgym'),
    url('^newchatroom/$', views.newchatroom, name='newchatroom'),

    url('^comment/(\d+)', views.comment, name='comment'),
    url('^joinchat/(\d+)', views.joinchat, name='joinchat'),
    url('^exitchat/(\d+)', views.exitchatroom(), name='exitchat'),
    # url('^connect/(?P<pk>\d+)',views.addfriend,name='addfriend'),
    # url('^unfriend/(?P<pk>\d+)', views.removefriend, name='removefriend'),
    url('^connect/(?P<operation>.+)/(?P<pk>\d+)',views.change_friends,name='change_friend'),
    url('^joingym/(\d+)', views.joingym, name='joingym'),
    url('^exitgym/(\d+)', views.exitgym, name='exitgym'),
]