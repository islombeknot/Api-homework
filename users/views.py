from django.shortcuts import render
from .serializers import SignUpSerializer
from rest_framework.generics import CreateAPIView
from .models import User, VIA_EMAIL , VIA_PHONE 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.validators import ValidationError
import datetime
from rest_framework.response import Response
from .utils import send_sms
# Create your views here.
class SignUpView(CreateAPIView):
     queryset = User.objects.all()
     serializer_class = SignUpSerializer

class Verifyview(APIView):
     permission_classes = (IsAuthenticated)

     def post(self, request):
          user = self.request.user
          if user is None:
               data ={
                    "status":False,
                    "massage":"Foydalanuvchi topilmadi"
               }
               raise ValidationError(data)

          if 'code' not in self.request.data:
               data = {
                    "status":False,
                    "massage":"Code maydoni majburiy "
               }
               raise ValidationError(data)
          code = self.request.data['code']
          
          verify_code = user.confirmation_codes.filter(is_confirmed=False,expire_time__gte=datetime.now(),code=code)
          
          if not verify_code.exists():
               data = {
                    "status":False,
                    "massage":"code eskirgan"

               }
               raise ValidationError(data)

          if user.auth_status == NEW:
               user.auth_status = CODE_VERIFIED
               user.save()

          data = {
               "auth_status":user.auth_status,
               "access":user.token()['access'],
               "refresh":user.token()['refresh'],
          }

          return Response(data)
     
class ResendVerifyView(APIView):
     permission_classes = (IsAuthenticated)

     def post(self, request):
          user = self.request.user
          if user.auth_type  == VIA_EMAIL:
               code = user.create_confirmation_code(VIA_EMAIL)
               send_sms(code)
          elif user.auth_type == VIA_PHONE:
               code = user.create_confirmation_code(VIA_PHONE)
               send_sms(code)
          else: 
                 data = {
                        "status":False,
                        "message":"siz bergan data xato"
                }
                 raise ValidationError(data)
          data = {
               "status":True,
               "message":"yuborildi"
          
          
          }
          return Response(data)





     def check_user_code(self,user):
          verify_code = user.confirmation_codes.filter(is_confirmed=False,expire_time__gte=datetime.now())
          if verify_code.exists():
               data = {
                    "status":False,
                    "message":"sizda hali kod mavjud"
               }
               raise ValidationError(data)