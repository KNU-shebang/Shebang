# coding: utf-8

from django.test import TestCase

from oneroom.models import Room, Comment
from account.models import User

class RoomAndCommentModelTest(TestCase):

    def test_saving_and_retrieving_rooms(self):
        user_ = User()
        user_.email = "blacksangi@gmail.com"
        user_.save()

        room1 = Room()
        room1.title = u"테크노문 원룸"
        room1.user = user_
        room1.content = u"기독센터 바로 뒤, 본관 10분거리"
        room1.location = u"테크노문"
        room1.rent = 30
        room1.start_date = "2017-03-01"
        room1.end_date = "2018-02-28"
        room1.save()

        room2 = Room()
        room2.title = u"북문 원룸"
        room2.user = user_
        room2.content = u"강남오뎅 지나서, 북문까지 10분거리"
        room2.location = u"북문"
        room2.rent = 35
        room2.start_date = "2017-05-21"
        room2.end_date = "2017-07-08"
        room2.save()

        comment1 = Comment()
        comment1.user = user_
        comment1.room = room1
        comment1.content = u"??????"
        comment1.save()

        comment2 = Comment()
        comment2.user = user_
        comment2.room = room1
        comment2.content = u"!!!!"
        comment2.save()

        saved_user = User.objects.first()
        self.assertEqual(saved_user, user_)

        saved_rooms = Room.objects.all()
        self.assertEqual(saved_rooms.count(), 2)
        
        first_saved_room = saved_rooms[0]
        second_saved_room = saved_rooms[1]
        self.assertEqual(first_saved_room.title, u'테크노문 원룸')
        self.assertEqual(first_saved_room.user, user_)
        self.assertEqual(first_saved_room.content, 
                         u'기독센터 바로 뒤, 본관 10분거리') 
        self.assertEqual(first_saved_room.location, u'테크노문')
        self.assertEqual(first_saved_room.rent, 30)
#        self.assertEqual(first_saved_room.start_date, '2017-03-01') 
#        self.assertEqual(first_saved_room.start_date, '2018-02-28')

        self.assertEqual(second_saved_room.title, u'북문 원룸')
        self.assertEqual(second_saved_room.user, user_)
        self.assertEqual(second_saved_room.content, 
                         u'강남오뎅 지나서, 북문까지 10분거리')
        self.assertEqual(second_saved_room.location, u'북문')
        self.assertEqual(second_saved_room.rent, 35)
#        self.assertEqual(second_saved_room.start_date, '2017-05-21')
#        self.assertEqual(second_saved_room.end_date, '2017-07-08')

        saved_comments = Comment.objects.all()
        self.assertEqual(saved_comments.count(), 2)

        first_saved_comment = saved_comments[0]
        second_saved_comment = saved_comments[1]

        self.assertEqual(first_saved_comment.user, user_)
        self.assertEqual(first_saved_comment.room, room1)
        self.assertEqual(first_saved_comment.content, u'??????')

        self.assertEqual(second_saved_comment.user, user_)
        self.assertEqual(second_saved_comment.room, room1)
        self.assertEqual(second_saved_comment.content, u'!!!!')

