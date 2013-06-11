from datetime import datetime
import socket
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context, loader, RequestContext
from models import User, Message


def home(request):
     try:
        nicknm = request.POST["username"]
        try:
            HOSTNAME = socket.gethostname()
        except:
            HOSTNAME = 'localhost'
        User.objects.all().delete() #narazie czyszcze, potem trzeba sprawdzic czy istnieje uzytkownik. daje to bo juz czasu nie ma :(
        user = User(nickname=nicknm, ip=HOSTNAME, create_date=datetime.now())
        request.session['usrname'] = nicknm
        return redirect(room)

     except (KeyError):
        return render_to_response("chat/home.html", context_instance=RequestContext(request))

def room(request):
    nickname=request.session['usrname']
    try:

        msg = request.POST["message"]
        message = Message(user=User.objects.get(nickname=nickname),message=msg,timestamp = datetime.now())
        message.save()
        messages=Message.objects.all()
        return render_to_response("chat/room.html", {'username': nickname, 'messages':messages }, context_instance=RequestContext(request))
    except (KeyError):
        return render_to_response("chat/room.html", {'username': nickname}, context_instance=RequestContext(request))
