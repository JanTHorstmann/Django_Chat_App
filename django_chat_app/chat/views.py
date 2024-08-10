from django.shortcuts import render, HttpResponseRedirect
from .models import Message, Chat
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        print('Received Data ' + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)

    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})

def login_view(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))

        if user:
            login(request, user)
            # return HttpResponseRedirect('/chat/')
            return HttpResponseRedirect(request.POST.get('redirect'))
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})

def register_view(request):
    redirect_url = request.GET.get('next', '/chat/')
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeatpassword = request.POST.get('repeatpassword')

        if password == repeatpassword:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
            if user:
                login(request, user)
                return HttpResponseRedirect(redirect_url)
        else:
            return render(request, 'auth/register.html', {'wrongPassword': True, 'redirect': redirect_url})
    return render(request, 'auth/register.html', {'redirect': redirect_url})