from django.conf.urls import url
from account import views

urlpatterns = [
# 회원 가입
    url(r'^signup/$', views.sign_up, name='signup'),
    # 이메일 인증 재요청
    url(r'^resend/$', views.resend_email, name='resend'),
    # 회원 메일 인증
    url(r'^(?P<user_name>[^/]+)/$', views.authorization, name='authorization'),
]