from django.core.mail import send_mail
from twilio.rest import Client

def send_verification_mail(email, token):
    try:
        send_mail(
            'email verification',
            f'http://127.0.0.1:8000/accounts/verify-token/{token}/',
            'admin@gmail.com',
            [f'{email}'],
            fail_silently=False
        )
        return True
    except:
        print("some unknown error occured")
        return False


def send_otp(phone, code):
    try:
        account_sid = "ACe827ae809d673fe9640975ff9e321dab"
        auth_token  = "cbec9b916ec7127248521af7e1561712" 
        
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to = f"+977{phone}", 
            from_ = "+15207794628",
            body = f"{code}")
        print(message.sid)
        return True
    except:
        return False