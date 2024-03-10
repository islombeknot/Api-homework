import datetime
from datetime import timedelta
import random
import uuid
from django.db import models
from  django.contrib.auth.models import AbstractUser


# Create your models here.
class BaseModel(models.Model):
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     class Meta:
          abstract = True

# USER TYPES
REGULAR = 'regular'
SUPPORT = 'support'
ADMIN = 'amin'

# AUTH STEPS
NEW = 'new'
CODE_VERIFIED = 'code_verified'
DONE = 'done'
IMAGE_STEP = 'image_step'

# USER REGISTER TYPES
VIA_PHONE = 'vie_phone'
VIA_EMAIL = 'via_email'



class User(BaseModel,AbstractUser):



     USER_ROLES = (
          (REGULAR,REGULAR),
          (SUPPORT,SUPPORT),
          (ADMIN,ADMIN)

     )

     AUTH_STEP_CHOICES = (
          (NEW,NEW),
          (CODE_VERIFIED,CODE_VERIFIED),
          (DONE,DONE),
          (IMAGE_STEP,IMAGE_STEP)
     )

     AUTH_TYPES_CHOICES = (
          (VIA_PHONE,VIA_PHONE),
          (VIA_EMAIL,VIA_EMAIL)
           
     )

     auth_type = models.CharField(max_length=20,choices=AUTH_TYPES_CHOICES)
     auth_status = models.CharField(max_length=20,choices=AUTH_STEP_CHOICES, default=NEW)
     user_role = models.CharField(max_length=20,choices=USER_ROLES, default=REGULAR)
     phone_number = models.CharField(max_length=13,unique=True,blank=True,null=True)
     email = models.EmailField(max_length=100, unique=True,blank=True,null=True)
     photo = models.ImageField(upload_to='user_images', blank=True, null=True)
     bio = models.CharField(max_length=255,blank=True,null=True)

     def __str__(self):
          return self.username
     
     @property
     def full_name(self):
          return f"{self.first_name} {self.last_name}"
     
def check_username(self):
     temp_username = self.username  # Initialize with current username
     if not temp_username:
        temp_username = f"telegram-{str(uuid.uuid4()).split('-')[-1]}"

     while User.objects.filter(username=temp_username).exists():
        temp_username = f"{temp_username}{random.randint(0, 9)}"

     self.username = temp_username


     def check_pass(self):
          if not self.password:
               temp_password = f"telegram-{str(uuid.uuid4()).split('-')[-1]}"
               self.password = temp_password
          
     def check_hash_password(self):
          if not self.password.startswith('pbkdf2_'):
               self.set_password(self.password)
     
     
     def save(self, *args, **kwargs):
          self.check_username()
          self.check_pass()
          self.check_hash_password()


          super(User,self).save(*args, **kwargs)    

     




class UserCodeVarivication(BaseModel):
     AUTH_TYPES_CHOICES = (
          (VIA_PHONE,VIA_PHONE),
          (VIA_EMAIL,VIA_EMAIL)
     )

     auth_type = models.CharField(max_length=20,choices=AUTH_TYPES_CHOICES)
     code = models.CharField(max_length=6)
     is_confirmed = models.BooleanField(default=False)
     expire_time = models.DateTimeField(null=True)
     user = models.ForeignKey('users.User',on_delete=models.CASCADE, related_name = 'confirmation_codes')

     def __str__(self):
          return f"{self.user.username} {self.code}"
     

def save(self, *args, **kwargs):
     if self.auth_type == VIA_EMAIL:
          self.expire_time = datetime.datetime.now() + timedelta(minutes=5)

     elif self.auth_type == VIA_PHONE:
          self.expire_time = datetime.datetime.now() + timedelta(minutes=2)
     
     super(UserCodeVarivication,self).save(*args, **kwargs)



     

               
     




        


         




     


