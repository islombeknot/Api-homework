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