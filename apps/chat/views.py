from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Room, Message
from django.contrib import messages
from django.shortcuts import redirect



def home(request):
    rooms = Room.objects.all()

    return render(request, 'chat/home_add.html',
                  {'rooms':rooms})

def room(request, room):
    username = request.GET.get('username')
    room_details = get_object_or_404(Room, name__iexact=room)
    return render(request, 'chat/room_add.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room_name = request.POST.get('room_name')
    username = request.POST.get('username')

    return redirect(f'/chat/{room_name}/?username={username}')

def getMessages(request, room):
    room_details = get_object_or_404(Room, name__iexact=room)
    messages = Message.objects.filter(room=room_details).order_by('created_at')

    data = []
    for msg in messages:
        data.append({
            "user": getattr(msg.user, "username", "Inconnu"),
            "value": msg.value,
            "image": msg.image.url if msg.image else None,
            "created": msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return JsonResponse({"messages": data})
