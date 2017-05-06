# coding: utf-8

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
import base64

from account.models import User
from account.forms import SignupForm, SendEmailForm
from .tasks import send_email_task



def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            form.save()
            send_email_task.delay(request.POST['email'], request.POST['name'])
                        
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
    

def resend_email(request):
    
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():
            send_email_task.delay(request.POST['email'], request.POST['name']) # 이메일 비동기 요청
            return redirect('root')

    else:
        form = SendEmailForm()

    return render(request, 'account/resend.html', {'form': form})
        