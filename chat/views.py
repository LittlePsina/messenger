# chat/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm
from .models import Chat, Message
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, LoginForm
from .models import Chat, Message
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def chat_view(request):
    chats = request.user.chats.all()
    return render(request, 'chat.html', {'chats': chats})

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.method == 'POST':
        message = Message.objects.create(chat=chat, sender=request.user, text=request.POST['message'])
        message.save()
    messages = chat.messages.all()
    return render(request, 'chat_detail.html', {'chat': chat, 'messages': messages})

@login_required
def create_chat(request):
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        name = request.POST.get('name')
        is_group = 'is_group' in request.POST
        chat = Chat.objects.create(name=name, is_group=is_group)
        chat.participants.add(request.user)

        participants_ids = request.POST.getlist('participants')
        participants = User.objects.filter(id__in=participants_ids)
        chat.participants.add(*participants)

        return redirect('chat')
    
    return render(request, 'create_chat.html', {'users': users})

def user_search(request):
    query = request.GET.get('user_search', '')
    users = User.objects.filter(username__icontains=query)[:10]
    html = render_to_string('user_search_results.html', {'users': users})
    return HttpResponse(html)