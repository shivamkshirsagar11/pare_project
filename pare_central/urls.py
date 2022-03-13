
from unicodedata import name
from django.urls import path
from . import views as v

urlpatterns = [
    path('',v.login,name="login" ),
    path('signup',v.signup,name="signup" ),
    path('home',v.home,name="homepage" ),
    path('change',v.change,name="" ),
    path('logout',v.logout,name="logout" ),
    path('addFriends',v.addFriend,name="addfriends" ),
    path('linkfriends',v.linkfriends,name="linkfriends" ),
    path('managereq',v.ManageRequest,name="requestManager" ),
    path('friends',v.friends,name="friends" ),
    path('manageBlocked',v.blocked,name="manageblocked" ),
    path('getchat',v.getmsg,name="getchat" ),
    path('sendchat',v.sendchat,name="chat" ),
    path('freq',v.showFrequest,name="freq" ),
    path('removechat',v.removemsg,name="remove" ),
    path('chat', v.chattest, name="chattest"),
    path('changeimg', v.changeimg, name="img"),
    path('chatrefresh', v.refresh, name="ref"),
    path('aboutus', v.about, name="about"),
]