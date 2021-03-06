# coding: utf-8

from django.db import models
from account.models import User
from oneroom.choices import TYPE_OF_ROOM


class Gate(models.Model):
    name_kr = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)

    def __str__(self):
        return "{0}({1})".format(self.name_kr, self.name_en)

class Room(models.Model):
    title = models.CharField(max_length=120)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    gate = models.ForeignKey(Gate, on_delete=models.CASCADE)
    content = models.TextField() # 추가정보
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=100) # 위치 정보
    room_type = models.CharField(max_length=20,
                                choices=TYPE_OF_ROOM, default=u"원룸")
    rent = models.PositiveIntegerField() # 월세
    deposit = models.PositiveIntegerField(default=0) # 보증금
    start_date = models.DateField() # 이어살기 시작 날짜
    end_date = models.DateField() # 이어살기 종료 날짜

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField(max_length=400, null=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room.title + " Comment, " + str(self.id)



