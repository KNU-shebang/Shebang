from django.conf.urls import url
from oneroom import views

urlpatterns = [
    # oneroom index 
    url(r'^$', views.IndexView.as_view(), name='index'),
    
    # 방 상세 페이지
    url(r'^room/(?P<pk>\d+)/$', views.RoomDetailView.as_view(),
        name='room'),
    
    # 방 신규 생성
    url(r'^room/new/$', views.room_new, name='room_new'),

    # 방 정보 수정
    url(r'^room/(?P<pk>\d+)/$', views.room_edit, name='room_edit'),

    # 댓글 달기
    url(r'^room/(?P<pk>\d+)/comment/new/$', views.comment_new, 
        name='comment_new'),
    
]

