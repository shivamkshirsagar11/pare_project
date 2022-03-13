from django.contrib import admin
from pare_central.models import BaseProfile,FullProfile,makeFriends,twousermessage

# Register your models here.
admin.site.register(BaseProfile)
admin.site.register(FullProfile)
admin.site.register(makeFriends)
admin.site.register(twousermessage)