# coding: utf-8

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
import base64

from account.models import User
from account.forms import SignupForm
# Create your views here.


def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            form.save()

            email = request.POST['email'].split('@')[0].encode('utf-8') # 사용자 인증 url로 이메일의 @ 앞부분을 base64 기반으로 인코딩
            encoded_email = base64.b64encode(email) # 인코딩
            from_email = settings.EMAIL_HOST_USER # 발신 메일 주소 - settings 파일에 지정(현재 임의)
            subject = '{} 님  회원가입 알림'.format(request.POST['name']) # 메일 제목
            to = request.POST['email'] # 수신 메일 주소 (사용자 회원가입 이메일)
            refined_email = str(encoded_email)[1:].strip("'") # 이메일 인코딩 값 b'c2F6MDU0OQ==' -> c2F6MDU0OQ==로 변경.
            html_content = """<h1>{0}님 가입을 환영합니다.</h1>
            <p>가입 인증을 위해서 아래 링크를 클릭해주세요</p>
            <a href='http://127.0.0.1:8000/account/{1}/'>http://127.0.0.1:8000/account/{2}/</a>
            
            """.format(request.POST['name'], refined_email, refined_email)
                 
            msg = EmailMessage( subject, html_content, from_email, [to]) 
            msg.content_subtype = "html"
            msg.send()

            return redirect('root')
    else:
        form = SignupForm()
    return render(request, 'account/signup.html', {'form': form})

def authorization(request, user_name):
    """  메일로 발송된 인증 url로 요청했을 때 작동하는 views """

    name = base64.b64decode(user_name.encode('utf-8')) # 인코딩되었던 email  name 부분을 디코딩 
    email = name.decode('utf-8') + '@knu.ac.kr' # 뒤에 knu.ac.kr를 붙여서 완전한 메일 구성

    user = User.objects.get(email=email) 
    user.is_active = True # active 값을 True로 변경.
    user.save()

    return redirect('root') 
    