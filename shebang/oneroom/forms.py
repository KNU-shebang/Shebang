# coding: utf-8

from django import forms
from django.conf import settings

from django_summernote.widgets import SummernoteWidget 

from oneroom.choices import TYPE_OF_ROOM
from oneroom.models import Room, Comment



class RoomForm(forms.ModelForm):
    title =forms.CharField(widget=forms.TextInput(attrs={'size':100}),
            label='제목')
    content = forms.CharField(widget=SummernoteWidget(), label='내용')
    
    
    location = forms.CharField(widget=forms.TextInput(attrs={'size':120, 
                'placeholder': '예) 대구광역시 북구 대학로 80'}), label='위치 정보')
    room_type = forms.ChoiceField(choices=TYPE_OF_ROOM, 
            widget=forms.Select(), label='방 종류')
    rent = forms.CharField(widget=forms.TextInput(attrs={'size':70}),
            label='월세')
    deposit = forms.CharField(widget=forms.TextInput(attrs={'size':70}),
            label='보증금', initial='0')
    start_date = forms.DateField(
            input_formats=settings.DATE_INPUT_FORMATS, label='시작일')
    end_date = forms.DateField(
            input_formats=settings.DATE_INPUT_FORMATS, label='종료일')

    class Meta:
        model = Room
        fields = ['title', 'location', 'room_type', 'rent',
                'deposit', 'start_date', 'end_date', 'content']
        

class CommentNew(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={'size':80}),
            label='댓글 입력')

    class Meta:
        model= Comment
        fields = ['content']

