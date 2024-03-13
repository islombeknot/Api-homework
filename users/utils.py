import requests
import threading
import re
from .models import User
from rest_framework.validators import ValidationError
phone_regex = r'^\+?\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}$'
email_regex = r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$'

def check_email_or_phone(user_input):
     if re.match(email_regex, user_input) is not None:
          return 'email'
     elif re.match(phone_regex, user_input) is not None:
          return 'phone'
     else :
          data = {
               "status":False,
               "message":"Valid email yoki phone number kiriting"

          }
          raise ValidationError(data)

class SmsThread(threading.Thread):

     def __init__(self, sms):
          self.sms = sms
          super(SmsThread, self).__init__()

     def run(self):
          send_message(self.sms)

def send_message(message_text):
     url = f'https://core.telegram.org/bots/api6735012647:AAHympVvmYnETcsa0Heo-_Iqlz2NZ1JcXKE/sendMassage'
     params = {
          'chat_id':"",
          'text':message_text,
     }

     response = requests.post(url, data=params)
     return response.json()

def send_sms(sms_text):
     sms_thread = SmsThread(sms_text)

     sms_thread.start()

     sms_thread.join()

