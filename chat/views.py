from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation, Chat
from core.models import Profile, User
from .forms import ConversationMessageForm
from django.db.models import OuterRef, Subquery, Max


# Create your views here.
# @login_required(login_url='login')
# def inbox(request):
#     conversations = Conversation.objects.filter(members__in=[request.user.id])
#
#     return render(request, 'chat/inbox.html', {'conversations': conversations})

def inbox(request):
    user = request.user
    conversations = Conversation.objects.filter(
        members__in=[user]
    ).annotate(
        latest_chat=Subquery(
            Chat.objects.filter(
                conversation=OuterRef('pk')
            ).order_by('-created_at').values('message')[:1]
        ),
        latest_chat_created_at=Subquery(
            Chat.objects.filter(
                conversation=OuterRef('pk')
            ).order_by('-created_at').values('created_at')[:1]
        ),
        other_user_profile=Subquery(
            User.objects.filter(
                conversations=OuterRef('pk')
            ).exclude(id=user.id).values('profile__profile_img')[:1]
        )
    )

    return render(request, 'chat/inbox.html', {'conversations': conversations})



@login_required(login_url='login')
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('chat:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'chat/detail.html', {
        'conversation': conversation,
        'form': form
    })

@login_required(login_url='login')
def new_chat(request, pk):
    messaging_user = get_object_or_404(Profile, user=request.user)

    messaged_user = get_object_or_404(Profile, user=User.objects.filter(username=pk).first())

    # conversations = Conversation.objects.filter(messaging_user=user).filter(members__in=[request.user.id])
    # if conversations:
    #     pass

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(messaging_user=messaged_user)
            conversation.members.add(request.user)
            conversation.members.add(messaged_user.user)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('/')

    else:
        form = ConversationMessageForm()

    return render(request, 'chat/chat.html', {'form': form})
