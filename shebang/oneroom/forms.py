# coding: utf-8

from django import forms
from django.conf import settings

from oneroom.choices import TYPE_OF_ROOM
from oneroom.models import Room, Comment

class RoomForm(forms.ModelForm):
    title =forms.CharField(widget=forms.TextInput(attrs={'size':100}),
            label='댓글 입력')
    content = forms.CharField(widget=forms.Textarea(attrs={'row':30, 
        'col':100}), label='내용')
    location = forms.CharField(widget=forms.TextInput(attrs={'size':120}),
            label='위치 정보')
    room_type = forms.ChoiceField(choices=TYPE_OF_ROOM, 
            widget=forms.RadioSelect(), label='방 종류')
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
        fields = ['title', 'content', 'location', 'room_type', 'rent',
                'deposit', 'start_date', 'end_date']


class CommentNew(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={'size':80}),
            label='댓글 입력')

    class Meta:
        model= Comment
        fields = ['content']

