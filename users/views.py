from django.conf import settings
from django.http import QueryDict
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.utils.html import escape
from django.contrib.auth.hashers import make_password

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

import uuid
from datetime import datetime, timedelta

from users.models import PasswordToken, UserProfile, UserSetting, User
from users.utils import email_user
from users.mixin import AccessMixin


# Create your views here.
class UsersViewAll(AccessMixin,View):
    def get(self, request):
        users = list(User.objects.values('id','username', 'email', 'is_staff','first_name'))
        
        context = { 
            'users': users,
            'action': {
                'name': 'User',
                'view_url': 'users:user_view',
                'edit_url': 'users:user_edit',
                'delete_url': 'users:user_delete',
                'create_url': 'users:user_create',
                'invite_url': 'users:user_invite',
            }
        }
        return render(request, 'users/users.html', context)

class UsersViewUser(AccessMixin,View):
    def get(self, request, pk):
        try:
            user = User.objects.values('id','username', 'email', 'is_staff','first_name','last_name','is_active').get(id=pk)
        
        except:
            messages.error(request, 'User does not exist')
            return redirect('users:users')
            
        context = {
            'page': 'view',
            'edit_user': user,
            'next': 'users:users'
        }
        return render(request, 'users/edit-user.html', context)

class UsersEditUser(AccessMixin,View):

    def get(self,request, pk):        
        try:
            user = User.objects.values('id','username', 'email', 'is_staff','first_name','last_name', 'is_active').get(id=pk)
               
        except Exception as err:
            print(err)
            messages.error(request, 'User does not exist')
            return redirect('users:users')
            
        context = {
            'page': 'edit',
            'edit_user': user,
            'next': 'users:users'
        }
        return render(request, 'users/edit-user.html', context)

    def post(self, request, pk):
        name=request.POST.get('name')
        last_name=request.POST.get('last_name')
        is_admin=request.POST.get('is_admin') 
        is_admin = True if is_admin else False
        is_active=request.POST.get('is_active') 
        is_active = True if is_active else False
        """  is_locked=request.POST.get('is_locked') 
        is_locked = True if is_locked else False """
        if name == "":
            messages.error(request, 'Name cannot be blank.')
            return redirect('users:users')
        try:
            user = User.objects.get(id=pk)
        except:
            messages.error(request, 'User does not exist')
            return redirect('users:users')
            
        user.first_name = name
        user.last_name = last_name
        user.is_staff = is_admin
        user.is_active = is_active
        #user.is_locked = is_locked
        user.save()
        return redirect('users:users')

class UsersDeleteUser(AccessMixin,View) :
    def delete(self,request, pk):     
        try:
            user = User.objects.filter(id=pk).delete()

        except:
            messages.error(request, 'User not found')
            return redirect('users:users')
        users = list(User.objects.values('id','username', 'email', 'is_staff','first_name'))
        
        context = { 
            'users': users,
            'action': {
                'name': 'User',
                'view_url': 'users:user_view',
                'edit_url': 'users:user_edit',
                'delete_url': 'users:user_delete',
                'create_url': 'users:user_create',
                'invite_url': 'users:user_invite',
            }
        }
        return render(request, 'users/partials/list-users.html', context)
    
class UsersCreateUser(AccessMixin,View):
    def get(self,request):
        context = {
           'next': 'users:users'
        }
        return render(request, 'users/create_user.html', context)

    def post(self, request):
        name = request.POST.get('name')
        last_name =request.POST.get('last_name')
        email = request.POST.get('email')
        is_staff = request.POST.get('is_staff')
        is_staff = True if is_staff else False
        #tmp_password = generate_password()
        uuid_str = uuid.uuid4()
        try:
            password_token = PasswordToken(name=name,last_name=last_name, email=email,is_staff=is_staff,token=uuid_str, token_life=1)
            print(password_token)
            password_token.save()
        except Exception as err:
            messages.error(request, 'Error creating password token for new user: ' + str(err))
            return redirect('users:users')

        if password_token == None:
            messages.error(request,'Error creating password token for new user.')
            return redirect('users:users')
            
        url = 'http://127.0.0.1:8000/users/create-password/' + str(uuid_str) + '?email=' + escape(email) + '&name=' + escape(name)
        html = """\
        Congratulations, """ + name + """!   You're account has been created.  Now create some encrtyped secrets to share!

        Please click the link below to activate your account and create a password.

        <a href=""" + url + """ >Activate your account.</a>
        """
        #response = email_user(email, html)

        #if response['result'] == 0:
        #    messages.error('Error sending email: ' + str(response['message']))

        return redirect('users:users')

class UsersResetPassword(View):
    def get(request, pk):
        user = User.objects.get(id=pk)
        
        if user == None:
            messages.error('User not found')
            redirect('core:index')

        context = {
            'user': user,
           'next': 'core:index'
        }
        return render(request, 'users/reset_password.html', context)

    def post(self, request,pk):
        user = User.objects.get(id=pk)
        
        if user == None:
            messages.error('User not found')
            redirect('core:index')
        name = user.first_name
        email = user.email
        user.password_expired = True
        user.save()
            
        uuid_str = uuid.uuid4()
        url = 'http://127.0.0.1:8000/users/create-password/' + str(uuid_str) + '?email=' + escape(email) + '&name=' + escape(name)
        print(url)
        html = """\
        Hello, """ + name + """.   Your password has expired.

        Please click the <a href=""" + url + """>link</a>  to create a new password.
        """
        response = email_user(email, html)

        if response['result'] == 0:
            messages.error('Error sending email: ' + str(response['message']))

        return redirect('core:index')
    
class UsersCreatePassword(View):
    def get(self,request, uuid):
        password_token = PasswordToken.objects.get(token=uuid)

        if password_token == None:
            msg = 'Cannot find token.'
            ctx = { 'uuid': uuid, 'name':  request.POST.get('name'),'last_name': request.POST.get('last_name'), 'email':  request.POST.get('email'), 'password': '', 'password_confirm': '','next': 'core:index', 'error': True, 'msg': msg}
            return render(request, 'users/create_password.html', ctx)

        #See if the token has expired
        timezone = password_token.created.tzinfo

        token_expired_time = password_token.created + timedelta(hours=password_token.token_life)
        is_token_expired = True if datetime.now(timezone) > token_expired_time else False

        if is_token_expired:
            messages.error(request, "Token has expired.")
        
        name = request.GET.get('name')
        email = request.GET.get('email')

        ctx = { 'uuid': uuid, 'name': name,'last_name':password_token.last_name, 'email': email, 'password': '', 'password_confirm': '','next': 'core:index', 'error': False, 'msg': ''}
        return render(request, 'users/create_password.html', ctx)

    def post(self, request, uuid):
        password_token = PasswordToken.objects.get(token=uuid)

        if password_token == None:
            msg = 'Cannot find token.'
            ctx = { 'uuid': uuid, 'name':  request.POST.get('name'),'last_name': request.POST.get('last_name'), 'email':  request.POST.get('email'), 'password': '', 'password_confirm': '','next': 'core:index', 'error': True, 'msg': msg}
            return render(request, 'users/create_password.html', ctx)

        name = password_token.name
        last_name = password_token.last_name
        email = password_token.email
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        is_staff = password_token.is_staff
        is_staff = True if is_staff else False
        password_changed = datetime.now()
            
        if password != password_confirm:
            msg = 'Passwords do not match'
            context = { 'uuid': uuid, 'name': name,'last_name': last_name, 'email': email, 'password': password, 'password_confirm': password_confirm,'next': 'core:index','error': True, 'msg': msg  }
            return render(request, 'users/create_password.html', context)

        try:
            password = make_password(password)
            user = User(username=email,first_name=name,last_name=last_name, email=email,password=password,is_staff=is_staff)
            full_name = name + ' ' + last_name
            user.save()
            #profile = UserProfile.objects.create(user=user,name=full_name,email=email)
            #profile.save()
            #user_settings = UserSetting(ttl=1,profile=profile)
            #user_settings.save()
        except Exception as err:
            print(err)
            msg = err
            context = { 'uuid': uuid, 'name': name,'last_name':last_name, 'email': email, 'password': '', 'password_confirm': '','next': 'core:index', 'error': True, 'msg': msg }
            return render(request, 'users/create_password.html', context)
        password_token.delete()
        return redirect('core:index')

class UsersInviteUser(AccessMixin,View):
    def get(self,request):
        context = {
           'next': 'users:users'
        }
        return render(request, 'users/invite_user.html', context)

    def post(self,request):
        name = request.POST.get('name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
            
        user = list(User.objects.filter(email=email).values())

        if len(user) > 1:
            messages.error(request, 'User already exists.')
            return redirect('users:users')
        uuid_str = uuid.uuid4()
        try:
            password_token = PasswordToken(name=name,last_name=last_name, email=email,is_staff=False,token=uuid_str, token_life=1)
            print(password_token)
            password_token.save()

        except Exception as err:
            messages.error(request, 'Error creating password token for new user: ' + str(err))
            return redirect('users:users')
        if password_token == None:
            messages.error(request,'Error creating password token for new user.')
            return redirect('users:users')
            
        url = 'http://127.0.0.1:8000/users/create-password/' + str(uuid_str) + '?email=' + escape(email) + '&name=' + escape(name)+ '&last_name=' + escape(last_name)
        html = """\
        Congratulations, """ + name + """!   You've been invited to join Secret Share!  Create encrypted secrets to share.

        Please click the link below to activate your account and create a password.

        <a href=""" + url + """ >Activate your account.</a>
        """
        #response = email_user(email, html)

        #if response['result'] == 0:
        #    messages.error(request, 'Error sending email: ' + str(response['message']))
            #messages.error(request, 'Error sending email: ' + str(response['smtp']))
            
        return redirect('users:users')

class ProfileViewProfile(AccessMixin,View):
    def get(self,request, pk):
        
        user = User.objects.get(id=pk)
        profile = user.userprofile
        user_settings = profile.usersetting
        
        context = { 'user_settings': user_settings   }

        return render(request, 'users/profile.html', context)

    def put(self, request, pk):
        user = User.objects.get(id=pk)
        profile = user.userprofile
        user_settings = profile.usersetting
        
        data = QueryDict(request.body).dict()
        user_settings.ttl = data['ttl']
        user_settings.save()
        context = { 'user_settings': user_settings,
                        'msg': 'Saved.'
        }
        return render(request, 'users/partials/save-success.html', context)

class UsersRegisterUser(View):
    def get(self,request):
        context = {
           'next': 'core:index'
        }
        return render(request, 'users/register_user.html', context)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name =request.POST.get('last_name')
        email = request.POST.get('email')
        is_staff = False
        uuid_str = uuid.uuid4()
        try:
            password_token = PasswordToken(name=first_name,last_name=last_name, email=email,is_staff=is_staff,token=uuid_str, token_life=5)
            password_token.save()
        except Exception as err:
            messages.error(request, 'Error creating password token for new user: ' + str(err))
            return redirect('users:users')

        if password_token == None:
            messages.error(request,'Error creating password token for new user.')
            return redirect('core:index')
            
        url = 'http://127.0.0.1:8000/users/create-password/' + str(uuid_str) + '?email=' + escape(email) + '&name=' + escape(first_name)
        html = """\
        Congratulations, """ + first_name + """!   You're account has been created.  Now create some encrtyped secrets to share!

        Please click the link below to activate your account and create a password.

        <a href=""" + url + """ >Activate your account.</a>
        """
        #response = email_user(email, html)

        #if response['result'] == 0:
        #    messages.error('Error sending email: ' + str(response['message']))

        #return redirect('core:index')
        next_url = reverse('users:user_create_password', args=[password_token.token ] )  + '?email=' + escape(email) + '&name=' + escape(first_name)
        return redirect(next_url)
        