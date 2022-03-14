import datetime
from django.db import models as m
class BaseProfile(m.Model):
    lastActive = m.CharField(max_length=25,default = "now")
    name = m.CharField(max_length=125,unique=True)
    email = m.EmailField(max_length=255,unique=True)
    password = m.CharField(max_length=500)
    usePurpose = m.TextField()
    def __str__(self):
        return self.name

class FullProfile(m.Model):
    bpu = m.ForeignKey(BaseProfile,on_delete = m.CASCADE)
    profileImg = m.ImageField(upload_to="user_profile",default="user_profile/default.jpg")
    address = m.TextField(max_length=255,default="not assigned")
    city = m.TextField(max_length=100,default="not assigned")
    pincode = m.IntegerField(default=0)
    firstname = m.CharField(max_length=155,default="pare")
    lastname = m.CharField(max_length=155,default="user")
    def __str__(self):
        return self.bpu.name
class makeFriends(m.Model):
    bpu = m.ForeignKey(BaseProfile,on_delete = m.CASCADE)
    requester = m.EmailField(max_length=255)
    requested = m.EmailField(max_length=255)
    status = m.TextField(max_length=25,default="requested")
    def __str__(self):
        return str(self.requester)+" -> "+str(self.requested)+" status: "+str(self.status)

class twousermessage(m.Model):
    date = m.CharField(max_length=25,default = "")
    messages = m.CharField(max_length=512,default="")
    userFrom = m.CharField(max_length=25,null=False)
    userTo = m.CharField(max_length=25,null=False)
    key = m.CharField(max_length=255,default="",null=False)
    def __str__(self):
        return str(self.userFrom)+"->"+str(self.userTo)
