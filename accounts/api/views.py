from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from ..serializers import UserSerializer, RegisterSerializer, LoginSerializer, ChangePasswordSerializer # RequestResetPasswordSerializer
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
# from ..utils import Mail
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.decorators import api_view, permission_classes
from ..send_mail import send_mail
import random
import json
from email.message import EmailMessage
import ssl
import smtplib

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer


    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def reset_password(request):
    email_sender='Bongasporti@gmail.com'
    password='ngivdclbbefhzxtj'

    email_receiver = 'nixonkipkorir01@gmail.com'
    subject = 'Password reset'
    body = """"Do you want to reset your Bongasport password?"""

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    



    return Response('working now')

# class RequestPasswordResetEmail(generics.GenericAPIView):
#     serializer_class = RequestResetPasswordSerializer
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         email = request.data['email']
        
#         if User.objects.filter(email=email).exists():
        
#             user = User.objects.filter(email=email)
#             userid64=urlsafe_base64_encode(smart_bytes(user.id))
#             token = PasswordResetTokenGenerator.make_token(user)
#             current_site=get_current_site(request=request).domain
#             relativeLink=reverse('reset-password', kwargs={'userid64':userid64, 'token':token})
#             absolute_url='http://'+current_site+relativeLink 

#             email_body='Hello, \n use this link to reset your password \n'+absolute_url
#             data={'email_body':email_body, 'to_email':user.email, 'email_subject':'Reset your password'}

#             Mail.send_email(data)

#             return attrs

#         return Response({'Success': 'We have just sent you a link to reset your password'}, status=status.HTTP_200_OK)

# class PasswordTokenCheckAPI(generics.GenericAPIView):
#     def get(self, request, userid64, token):
#         pass