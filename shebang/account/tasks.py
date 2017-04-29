from celery.decorators import task
from celery.utils.log import get_task_logger
from account.views import send_signup_email

logger = get_task_logger(__name__)

@task(name='send_email_task')
def send_email_task(email, name):
    logger.info("가입 확인 이메일 전송하기")

    return send_signup_email(email, name)