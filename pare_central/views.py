from base64 import b64encode
import base64
import datetime
import email
from cryptography.fernet import Fernet
from pickle import NONE
import random
from unicodedata import name
from django.shortcuts import render,redirect,HttpResponse
from pare_central.models import BaseProfile as bp,FullProfile as fp,makeFriends,twousermessage
from django.contrib import messages
import bcrypt
from django.core.cache import cache
from django.http import HttpRequest, JsonResponse
from django.utils.cache import get_cache_key
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils.crypto import get_random_string

def logout(request):
    try:
        ins_user = bp.objects.filter(email=request.session["email"]).first()
        ins_user.lastActive = datetime.datetime.now().strftime("%H:%M:%S%p")
        ins_user.save()
        request.session["email"] = "Unverified"
        return redirect("/")
    except:
        return redirect("/")
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        request.session["email"] = email
        ins_user = bp.objects.filter(email=email).first()
        
        if ins_user:
            request.session["name"] = ins_user.name 
            ins_user_full = fp.objects.filter(bpu_id = ins_user.id).first()
            
            if bcrypt.checkpw(password.encode('utf-8'), ins_user.password.encode('utf-8')):
                name  = request.session["name"]
                otherReq = makeFriends.objects.filter(requested = name,status="requested")
                friends =  makeFriends.objects.filter(requester = ins_user.name,status = "friend")
                print(friends)
                picsoffriends = []
                for i in friends:
                    bpu = bp.objects.get(name = i.requested)
                    fpu = fp.objects.get(bpu = bpu)
                    msg = twousermessage.objects.filter(Q(userFrom = i.requested,userTo= ins_user.name) | Q(userTo = i.requested,userFrom= ins_user.name)).last()
                    temp = str(fpu.profileImg)
                    if msg is None:
                        temp2 = {"friendBase":bpu,"pic":temp,"msg":"start chat with "+i.requested+" now!","friendFull":fpu,"time":""}
                    else: 
                        key = msg.key
                        tempmsg = msg.messages
                        fernet = Fernet(key.encode())
                        msg.messages = fernet.decrypt(tempmsg.encode()).decode()
                        temp2 = {"friendBase":bpu,"pic":temp,"msg":msg.messages,"friendFull":fpu,"time":msg.date}
                    picsoffriends.append(temp2)
                otherpic = []
                for i in otherReq:
                    bpu = bp.objects.get(name = i.requester)
                    fpu = fp.objects.get(bpu = bpu)
                    temp = str(fpu.profileImg)
                    temp2 = {"obj":i, "objimg":temp}
                    otherpic.append(temp2)

                return render(request, 'home.html',{"user":ins_user,"fullp":ins_user_full,"data":picsoffriends,"other":otherpic})
            else:
               messages.error(request,'Password is not matching !')
               return redirect('/')
        else:
            messages.error(request,'No user found with this email !')
            return redirect('/')
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['pass']
        use = request.POST['type']
        temp = bp.objects.filter(name=name).first()
        temp2 = bp.objects.filter(email=email).first()
        if temp is not None:
            messages.error(request,"Username is already taken !")
            return redirect('/signup')
        if temp2 is not None:
            messages.error(request,"Email already exist !")
            return redirect('/signup')
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
        basep = bp(name=name,email=email,usePurpose=use,password=hashed_pw.decode('utf-8'))
        basep.save()
        fullp = fp(firstname = basep.name,bpu = basep)
        fullp.save()
        messages.success(request,"Your account created successfully!")
        return redirect('/')
    return render(request, 'registration.html')
def changeimg(request):
    email =  request.session["email"] if request.session["email"] != "Unverified" else "Unverified"
    if email == "Unverified" : return redirect("/")
    else:
        ins_user = bp.objects.filter(email=email).first()
        ins_user_full = fp.objects.filter(bpu_id = ins_user.id).first()
        if ins_user:
            if request.method == 'POST':
                image = request.FILES['userImg']
                ins_user_full.profileImg = image
                ins_user_full.save()
                friends =  makeFriends.objects.filter(requester = ins_user.name,status = "friend")
                return render(request, 'home.html',{"user":ins_user,"fullp":ins_user_full,"friends":friends})
            return render(request, '/',{"user":ins_user,"fullp":ins_user_full})


def change(request):
    email =  request.session["email"] if request.session["email"] != "Unverified" else "Unverified"
    if email == "Unverified" : return redirect("/")
    else:
        ins_user = bp.objects.filter(email=email).first()
        ins_user_full = fp.objects.filter(bpu_id = ins_user.id).first()
        if ins_user:
            if request.method == 'POST':
                name = request.POST['name']
                email = request.POST['email']
                use = request.POST['use']
                address = request.POST['address']
                city = request.POST['city']
                pincode = request.POST['pin']
                fname = request.POST['fname']
                lname = request.POST['lname']
                #if request.POST['picselect'] == "Yes":
                 #   image = request.FILES['userImg']
                  #  ins_user_full.profileImg = image 

                ins_user.name = name
                ins_user.email = email
                ins_user.usePurpose = use
                ins_user.save()

                ins_user_full.address = address
                ins_user_full.city = city
                ins_user_full.pincode = pincode
                ins_user_full.firstname = fname
                ins_user_full.lastname = lname
                ins_user_full.save()
                friends =  makeFriends.objects.filter(requester = ins_user.name,status = "friend")
                
                picsoffriends = []
                for i in friends:
                    bpu = bp.objects.get(name = i.requested)
                    fpu = fp.objects.get(bpu = bpu)
                    msg = twousermessage.objects.filter(Q(userFrom = i.requested,userTo= ins_user.name) | Q(userTo = i.requested,userFrom= ins_user.name)).last()
                    temp = str(fpu.profileImg)
                    if msg is None: 
                        temp2 = {"friendBase":bpu,"pic":temp,"msg":"start chat with "+i.requested+" now!","friendFull":fpu,"time":""}
                    else: 
                        key = msg.key
                        tempmsg = msg.messages
                        fernet = Fernet(key.encode())
                        msg.messages = fernet.decrypt(tempmsg.encode()).decode()
                        temp2 = {"friendBase":bpu,"pic":temp,"msg":msg.messages,"friendFull":fpu,"time":""}
                    picsoffriends.append(temp2)
                return render(request, 'home.html',{"user":ins_user,"fullp":ins_user_full,"data":picsoffriends})
            return render(request, 'changeprofile.html',{"user":ins_user,"fullp":ins_user_full})

def home(request):
    if request.method != 'POST' and request.session["email"] != "Unverified":
        ins_user = bp.objects.filter(email=request.session["email"]).first()
        ins_user_full = fp.objects.filter(bpu=ins_user).first()
        name  = request.session["name"]
        otherReq = makeFriends.objects.filter(requested = name,status="requested")
        friends =  makeFriends.objects.filter(requester = ins_user.name,status = "friend")
        print(friends)
        picsoffriends = []
        for i in friends:
            bpu = bp.objects.get(name = i.requested)
            fpu = fp.objects.get(bpu = bpu)
            msg = twousermessage.objects.filter(Q(userFrom = i.requested,userTo= name) | Q(userTo = i.requested,userFrom= name)).last()
            temp = str(fpu.profileImg)
            if msg is None: 
                temp2 = {"friendBase":bpu,"pic":temp,"msg":"start chat with "+i.requested+" now!","friendFull":fpu,"time":""}
            else: 
                key = msg.key
                tempmsg = msg.messages
                fernet = Fernet(key.encode())
                msg.messages = fernet.decrypt(tempmsg.encode()).decode()
                temp2 = {"friendBase":bpu,"pic":temp,"msg":msg.messages,"friendFull":fpu,"time":""}
            picsoffriends.append(temp2)
        otherpic = []
        for i in otherReq:
            bpu = bp.objects.get(name = i.requester)
            fpu = fp.objects.get(bpu = bpu)
            temp = str(fpu.profileImg)
            temp2 = {"obj":i, "objimg":temp}
            otherpic.append(temp2)

        return render(request, 'home.html',{"user":ins_user,"fullp":ins_user_full,"data":picsoffriends,"other":otherpic})
    else: return redirect('/')

def addFriend(request):
    if request.method == 'POST':
        name = request.POST['name']
        print(name)
        fulluser = fp.objects.values().filter(firstname__icontains=name)
        fulluser2 = fp.objects.filter(firstname__icontains = name)
        if fulluser2.exists():
            fulluser_list = list(fulluser)
            halful = []
            img = []
            for i in fulluser2:
                halfu = bp.objects.filter(id = i.bpu_id).first()
                name = halfu.name
                halful.append(name)
            return JsonResponse({"msg":"found user with username that you've entered","userList":fulluser_list,"halfusr":halful})
        else: return JsonResponse({"msg":"No user found with that name!!"})
@csrf_exempt
def linkfriends(request):
    if request.method == 'POST':
        name = request.POST['name'] if request.POST['name'] != request.session["name"] else "user"
        if name == "user": return JsonResponse({"msg":"User"})
        else:
            friend = makeFriends.objects.filter(requester = request.session["name"],requested = name).first()
            if friend is not None: 
                friend2 = makeFriends.objects.filter(requested = request.session["name"],requester = name).first()
                if friend2 is not None : 
                    if friend.status == "Blocked": return JsonResponse({"msg":"Blocked"})
                    elif friend.status == "Unavailable": return JsonResponse({"msg":"Unavailable"})
                    elif friend.status == "Unavailable-sent": return JsonResponse({"msg":"Unavailable"})
                    return JsonResponse({"msg":"Already friend!"})
                return JsonResponse({"msg":"req sent"}) 
            friend = makeFriends.objects.filter(requested = request.session["name"],requester = name,status = "requested").first()
            if friend is not None: 
                return JsonResponse({"msg":"already sent you request","name":name})
            ins_user = bp.objects.filter(name = request.session["name"]).first()
            makeList = makeFriends(bpu = ins_user,requester = request.session["name"],requested = name)
            makeList.save()
            return JsonResponse({"msg":"Request sent successfully!"})


def ManageRequest(request):
    if request.method == "POST":
        if request.POST['Manage'] == "Accept":
            requested = request.session["name"]
            requester = request.POST['Othername']
            bpu = bp.objects.get(name=requester)
            fpu = fp.objects.get(bpu = bpu)
            name = bpu.name
            fname = fpu.firstname
            img = str(fpu.profileImg)
            ll = bpu.lastActive
            msg = "start chat with "+ str(fpu.firstname) + "!"
            data = {"name":name, "msg":msg, "img":img, "ll":ll, "fname":fname }
            friend = makeFriends.objects.filter(requested = requested,requester = requester).first()
            if friend is not None : 
                friend.status = "friend"
                friend.save()
                ins_user = bp.objects.filter(name = request.session["name"]).first()
                newfriend = makeFriends(bpu = ins_user,requester = requested,requested = requester,status = "friend")
                newfriend.save()
                return JsonResponse(data)
        if request.POST['Manage'] == "Decline":
            requested = request.session["name"]
            requester = request.POST['Othername']
            friend = makeFriends.objects.filter(requested = requested,requester = requester).first().delete()
            return HttpResponse("Done")

        if request.POST['Manage'] == "Block":
            requested = request.session["name"]
            requester = request.POST['Othername']
            print(requester,requested)
            friend = makeFriends.objects.filter(requested = requested,requester = requester).first()
            if friend is not None : 
                friend.status = "Unavailable"
                friend.save()
                ins_user = bp.objects.filter(name = request.session["name"]).first()
                newfriend = makeFriends(bpu = ins_user,requester = requested,requested = requester,status = "Blocked")
                newfriend.save()
                return HttpResponse("Done")
            else:
                friend = makeFriends.objects.filter(requested = requester,requester = requested).first()
                friend.status = "Blocked"
                friend.save()
                ins_user = bp.objects.filter(name = requester).first()
                newfriend = makeFriends(bpu = ins_user,requested = requested,requester = requester,status = "Unavailable-sent")
                newfriend.save()
                return HttpResponse("Done")
            
        if request.POST['Manage'] == "Unfriend":
            requested = request.session["name"]
            requester = request.POST['Othername']
            friend = makeFriends.objects.filter(requested = requester,requester = requested).first().delete()
            return HttpResponse("Done")
        if request.POST['Manage'] == "Unfriend-friend":
            print("callable")
            requested = request.session["name"]
            requester = request.POST['Othername']
            makeFriends.objects.filter(requested = requester,requester = requested).first().delete()
            friend = makeFriends.objects.filter(requested = requested,requester = requester).first()
            friend.status = "requested"
            friend.save()
            
            return HttpResponse("Done")
        if request.POST['Manage'] == "Block-friend":
            requested = request.session["name"]
            requester = request.POST['Othername']
            friend = makeFriends.objects.filter(requested = requested,requester = requester).first()
            if friend is not None : 
                friend.status = "Unavailable"
                friend.save()
                friend2 = makeFriends.objects.filter(requested = requester,requester = requested).first()
                friend2.status = "Blocked"
                friend2.save()
                return HttpResponse("Done")

        if request.POST['Manage'] == "Unblock-friend":
            requested = request.session["name"]
            requester = request.POST['Othername']
            print(requester,requested)
            friend = makeFriends.objects.filter(requested = requested,requester = requester).first()
            print(friend)
            if friend is not None :
                if friend.status == "Unavailable-sent": 
                    friend.delete()
                    makeFriends.objects.filter(requester = requested,requested = requester).first().delete()
                else: 
                    friend.status = "requested"
                    friend.save()
                makeFriends.objects.filter(requested = requester,requester = requested).first().delete()
                return HttpResponse("Done")


def friends(request):
    name  = request.session["name"]
    myReq = makeFriends.objects.filter(requester = name,status="friend")
    return render(request,'friends.html',{"my":myReq})

def blocked(request):
    name  = request.session["name"]
    myReq = makeFriends.objects.filter(requester = name,status="Blocked")
    return render(request,'blocked.html',{"my":myReq})

def sendchat(request):
    chatfrom = request.POST['ufrom']
    chatto = request.POST['to']
    message2 = request.POST['message']
    key = Fernet.generate_key()
    fernet = Fernet(key)
    message = fernet.encrypt(message2.encode())
    messageObj = twousermessage(userFrom = chatfrom,userTo = chatto,messages = message.decode(),date = datetime.datetime.now().strftime("%I:%M%p"),key=key.decode())
    messageObj.save()
    return HttpResponse("Message sent")
@csrf_exempt
def getmsg(request):
    if request.method == "POST":
        ufrom = request.session['name']
        uto = request.POST['touser']
        chatmsg =  twousermessage.objects.values().filter(Q(userFrom = ufrom,userTo = uto) | Q(userTo = ufrom,userFrom = uto))
        # chatmsg2 =  twousermessage.objects.filter(Q(userFrom = ufrom,userTo = uto) | Q(userTo = ufrom,userFrom = uto))
        litemp = []
        for i in chatmsg:
            key = i['key']
            msg = i['messages']
            # base64.urlsafe_b64decode(key)
            fernet = Fernet(key.encode())
            i['messages'] = fernet.decrypt(msg.encode()).decode()
        print(chatmsg)
        li = list(chatmsg)
        ins_user = bp.objects.filter(name=uto).first()
        ins_user_full = fp.objects.values().filter(bpu_id = ins_user.id).first()
        ins_user = bp.objects.values().filter(name =uto).first()
        return JsonResponse({"msg":li, "friend_fpu": ins_user_full, "friend_bpu":ins_user})

def chattest(request):
    return render(request, 'chat_ui.html')
@csrf_exempt
def changeimg(request):
    email =  request.session["email"] if request.session["email"] != "Unverified" else "Unverified"
    if email == "Unverified" : return redirect("/")
    else:
        ins_user = bp.objects.filter(email=email).first()
        ins_user_full = fp.objects.filter(bpu_id = ins_user.id).first()
        if ins_user:
            if request.method == 'POST':
                image = request.FILES['userImg']
                print(image)
                ins_user_full.profileImg = image
                ins_user_full.save()
            return HttpResponse("done")

def showFrequest(request):
    if request.method == 'POST':
        name  = request.session["name"]
        otherReq = makeFriends.objects.values().filter(requested = name,status="requested")
        otherReq2 = makeFriends.objects.filter(requested = name,status="requested")
        piclist = []
        for i in otherReq2:
            tempb = bp.objects.get(name=i.requester)
            tempf = fp.objects.get(bpu = tempb)
            pic = str(tempf.profileImg)
            piclist.append(pic)
        myReq = makeFriends.objects.values().filter(requester = name,status="requested")
        myReq2 = makeFriends.objects.filter(requester = name,status="requested")
        friends = makeFriends.objects.values().filter(requester = name,status="friend")
        friends2 = makeFriends.objects.filter(requester = name,status="friend")
        blocked = makeFriends.objects.values().filter(requester = name,status="Blocked")
        blocked2 = makeFriends.objects.filter(requester = name,status="Blocked")
        mypiclist = []
        for i in myReq2:
            tempb = bp.objects.get(name=i.requested)
            tempf = fp.objects.get(bpu = tempb)
            pic = str(tempf.profileImg)
            mypiclist.append(pic)
        friendpic=[]
        for i in friends2:
            tempb = bp.objects.get(name=i.requested)
            tempf = fp.objects.get(bpu = tempb)
            pic = str(tempf.profileImg)
            friendpic.append(pic)
        blockedfriendpic=[]
        for i in blocked2:
            tempb = bp.objects.get(name=i.requested)
            tempf = fp.objects.get(bpu = tempb)
            pic = str(tempf.profileImg)
            blockedfriendpic.append(pic)
        
        return JsonResponse({"other":list(otherReq),"my":list(myReq),"picsother":piclist,"picsmy":mypiclist,"friend":list(friends),"friendpic":friendpic,"blocked":list(blocked),"blockedfriendpic":blockedfriendpic})

def removemsg(request):
    if request.method == "POST":
        id = request.POST['id']
        twousermessage.objects.filter(id = id).first().delete()
        return HttpResponse("Done")

def refresh(request):
    if request.method == "POST":
        name = request.session['name']
        friends2 = makeFriends.objects.filter(requester=name,status="friend")
        friendpic = []
        for i in friends2:
            bpu = bp.objects.get(name = i.requested)
            bpu2 = bp.objects.values().filter(name = i.requested).first()
            fpu2 = fp.objects.values().filter(bpu = bpu).first()
            msgtemp = twousermessage.objects.filter(Q(userFrom = i.requested,userTo= name) | Q(userTo = i.requested,userFrom= name)).last()
            if msgtemp is not None:
                friendpic.append({"fbase":bpu2,"ffull":fpu2,"lastmsg":msgtemp.messages,"time":msgtemp.date})
            else: 
                friendpic.append({"fbase":bpu2,"ffull":fpu2,"lastmsg":"start chat with "+str(i.requested)+" now!","time":""})
        return JsonResponse({"data":friendpic})

def about(request):
    return render(request,"aboutus.html")