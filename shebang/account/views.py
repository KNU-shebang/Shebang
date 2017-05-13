# coding: utf-8

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.hashers import check_password 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
import base64

from account.models import User
from account.forms import SignupForm, SendEmailForm, ChangePasswordForm, LoginForm
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

def get_user(email):
    
    try:
        return User.objects.get(email=email)

    except User.DoesNotExists:
        return None

def login(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            existed_user = get_user(request.POST['email'])

            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    messages.success(request, '로그인되었습니다.')
                    return redirect('/')

            elif user is None and existed_user is not None:
                messages.error(request, '이메일 인증절차가 필요합니다.')

            elif user is None and existed_user is None:
                messages.error(request, '가입되지 않은 사용자입니다.')

        else:
            messages.error(request, '올바른 정보를 입력해주세요.')
    
    else:
        form = LoginForm()

    return render(request, 'account/login.html', { 'form': form })

def logout(request):
    
    django_logout(request)
    messages.success(request, '로그아웃 되었습니다.')

    return redirect('/')
                 

@login_required
def change_password(request):

    user = User.objects.get(email=request.user.email)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if check_password(request.POST['password'], user.password): #현재 비밀번호 확인
                print('Okay')
                user.set_password(request.POST['password1'])  # 새로운 비밀번호 저장.
                user.save()
                return redirect('root')
            else:
                print('Fail to change password') # message로 에러 발생 시키기        
    else:
        form = ChangePasswordForm()
    
    return render(request, 'account/change.html', {'form': form})
