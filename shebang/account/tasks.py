from django.core.mail import EmailMessage
from celery.decorators import task
from django.conf import settings
import base64






@task(name='send_email_task')
def send_email_task(email, name):
    
    email_value = email.split('@')[0].encode('utf-8') # 사용자 인증 url로 이메일의 @ 앞부분을 base64 기반으로 인코딩
    encoded_email = base64.b64encode(email_value) # 인코딩
    from_email = settings.EMAIL_HOST_USER # 발신 메일 주소 - settings 파일에 지정(현재 임의)
    subject = '{} 님  회원가입 알림'.format(name) # 메일 제목
    refined_email = str(encoded_email)[1:].strip("'") # 이메일 인코딩 값 b'c2F6MDU0OQ==' -> c2F6MDU0OQ==로 변경.
    html_content = """<h1>{0}님 가입을 환영합니다.</h1>
    <p>가입 인증을 위해서 아래 링크를 클릭해주세요</p>
    <a href='http://127.0.0.1:8000/account/{1}/'>http://127.0.0.1:8000/account/{2}/</a>
    
    """.format(name, refined_email, refined_email)
            
    msg = EmailMessage( subject, html_content, from_email, [email]) 
    msg.content_subtype = "html"
    msg.send()
