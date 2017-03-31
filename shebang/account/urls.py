from django.conf.urls import url
from account import views

urlpatterns = [
# 회원 가입
    url(r'^signup/$', views.sign_up, name='signup'),

    # 회원 메일 인증
    url(r'^(?P<user_name>[^/]+)/$', views.authorization, name='authorization'),
]