import smtplib

from django.core.mail import send_mail
from django.template.loader import render_to_string

from app_celery.celery import app


@app.task
def send_email(subject, from_email, to_email, template, args):

    html_message = render_to_string(template, args)
    try:
        send_mail(subject=subject, message='', from_email=from_email,
                  recipient_list=[to_email], html_message=html_message)
    except smtplib.SMPTException:
        print(f'Error while sending email to {to_email}')

