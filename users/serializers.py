from django.db.models import Q
from rest_framework import serializers
from .models import User, VIA_PHONE, VIA_EMAIL
from .utils import check_email_or_phone, send_sms
from rest_framework.exceptions import ValidationError

class SignUpSerializer(serializers.ModelSerializer):
     auth_type = serializers.CharField(required=False, read_only=True)
     auth_status = serializers.CharField(required=False, read_only=True)
     
     def __init__(self,*args, **kwargs):
          super(SignUpSerializer, self).__init__(*args, **kwargs)
          self.fields['email_phone']=serializers.CharField(required=True)
  
     

     class Meta:
          model = User
          fields = ('auth_type', 'auth_status' )


     def validate_email_phone(self,email_phone):
          user = User.objects.filter(Q(email=email_phone) | Q(phone_number=email_phone))

          if user.exists():
               data = {
                    "status":False,
                    "message":"foydalanuvchi mavjud"
               }
               raise ValidationError(data)
          return email_phone

          
                


     def validate(self, data):
          user_input = data.get('email_phone')
          email_or_phone = check_email_or_phone(user_input)
          if email_or_phone == 'phone':
               data = {
                    'auth_type':VIA_PHONE,
                    'phone_number':user_input
               }
          elif email_or_phone == 'email':
                        data = {
                    'auth_type':VIA_EMAIL,
                    'phone_number':user_input
               }
          else: 
                 data = {
                        "status":False,
                        "message":"siz bergan data xato"
                 }
          raise ValidationError(data)

          return data
     def create(self, validated_data):
            user = super(SignUpSerializer,self).create(validated_data)

            auth_type = validated_data.get('auth_type')

            if auth_type == VIA_EMAIL:
               code = user.create_confirmation_code(VIA_EMAIL)
               send_sms(code)

            elif auth_type == VIA_PHONE:
               code = user.create_confirmation_code(VIA_EMAIL)
               send_sms(code)
            else:
               data = {
                        "status":False,
                        "message":"kode yuborishda xatolik boldi"
                 }
               raise ValidationError(data)
                  

     def to_representation(self, instance):
        data = super(SignUpSerializer,self).to_representation(instance)
        
        data['access'] = instance.token()['access']
        data['refresh'] = instance.token()['refresh']
     
        return data
     