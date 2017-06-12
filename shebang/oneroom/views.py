from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from oneroom.models import Room, Gate
from oneroom.forms import RoomForm, CommentNew
from account.models import User



class IndexView(ListView):
    """oneroom app index"""
    template_name = 'oneroom/index.html'
    model = Room

def board(request, gate_name):
    
    rooms = Room.objects.filter(gate__name_en=gate_name)
    return render(request, 'oneroom/board.html', {'gate_name': gate_name,
                                                    'rooms': rooms })

class RoomDetailView(DetailView):
    """Room 상세 페이지"""
    model = Room

    def get_context_data(self, **kwargs):
        context = super(RoomDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentNew
        return context


def room_new(request):
    """Room 생성"""

    gates = Gate.objects.all()
    if request.method == 'POST':
        print(request.user)
        form = RoomForm(request.POST)
        if form.is_valid():
            print(form)
            gate = Gate.objects.get(id=request.POST['gate'])
            room = Room.objects.create(title=request.POST['title'],
                        user=request.user,
                        gate=gate,
                        content=request.POST['content'],
                        location=request.POST['location'],
                        room_type=request.POST['room_type'],
                        rent=request.POST['rent'],
                        deposit=request.POST['deposit'],
                        start_date=request.POST['start_date'],
                        end_date=request.POST['end_date'])
            
            
            return redirect('oneroom:room', pk=room.pk)

    else:
        form = RoomForm()
        
    return render(request, 'oneroom/room_new.html', {'form': form, 
                                                    'gates': gates })


def room_edit(request, pk):
    """룸 수정"""
    room = get_object_or_404(Room, pk=pk)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            room = form.save(commit=False)
            room.user = request.user.id
            room.save()
            return redirect('oneroom:room', pk=room.pk)

    else:
        form = RoomForm(instance=room)
    return render(request, 'oneroom/room_edit.html', {'form': form})


def comment_new(request, pk):
    if request.method == 'POST':
        form = CommentNew(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.room = Room.objects.get(pk=pk)
            comment.user = request.user
            comment.save()
            return redirect('oneroom:room', pk)

    else:
        form = CommentNew()
    return render(request, 'room_detail.html', {
        'form': form,
        'pk': pk,
        })

