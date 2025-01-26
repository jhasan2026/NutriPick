from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name='public-chat')
    chat_messages = chat_group.chat_messages.all()[:30]

    form = ChatmessageCreateForm()

    if request.method == "POST":
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            return redirect('chat')

    context = {
    'chat_messages' : chat_messages,
    'form' : form,
    }
    return render(request, 'a_rtchat/chat.html',context)