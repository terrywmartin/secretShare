from distutils.log import Log
from multiprocessing import sharedctypes
from django.shortcuts import redirect, render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from datetime import datetime

from .forms import SharedSecretForm
from .models import SharedSecret
from users.utils import email_user
from users.models import User


# Create your views here.
class SecretsAddSecret(View):
    def get(self, request):
        form = SharedSecretForm()
        if request.user.is_authenticated:
            profile = request.user.userprofile
            settings = profile.usersetting
        else:
            settings = { "ttl": 1}
        context = {
            'secret': '',
            'next': 'secrets:secrets',
            'form': form,
            'usersettings': settings
        }
       
        return render(request, 'encryptedSecrets/add_secret.html', context)
    def post(self, request):
        
        plain_secret = request.POST.get('secret')
        name = request.POST.get('name')
        ttl = request.POST.get('ttl') if request.user.is_authenticated else 1
        sharedsecret = SharedSecret(name=name,text=plain_secret,ttl=ttl)

        if request.user.is_authenticated:
            sharedsecret.owner = request.user
            redirect_url = 'encryptedSecrets:secrets'
        else:
            sharedsecret.owner = None
            redirect_url = reverse('encryptedSecrets:secret_view' , args=[sharedsecret.id])
            print(redirect_url)
        
        sharedsecret.save()

        return redirect(redirect_url)

class SecretsViewSecret(View):
    def get(self,request, pk):
        try:
            sharedsecret = SharedSecret.objects.get(id=pk)
        except:
            return render(request, 'encryptedSecrets/notfound.html')
        accessed = sharedsecret.accessed
        msg = ''
    
        if not request.user.is_authenticated:
            ttl = 1

        else:
            ttl = sharedsecret.ttl

        clicksLeft = ttl - accessed
        context = {
            'secret': sharedsecret,
            'next': 'secrets:secrets',
            'page': 'view',
            'msg': msg,
            'clicksLeft': clicksLeft
        }
    
        return render(request, 'encryptedSecrets/view_secret.html', context)

    def post(self, request, pk):
        try:
            sharedsecret = SharedSecret.objects.get(id=pk)
        except:
            return render(request, 'encryptedSecrets/notfound.html')
        accessed = sharedsecret.accessed
        msg = ''
            
        if request.user.is_authenticated:
            email = request.POST.get('email')
            if email == "":
                return render(request, 'encryptedSecrets/partials/sent_failure.html')    
                
            response = email_secret(email, request.build_absolute_uri())
            if response:
                return render(request, 'encryptedSecrets/partials/sent_success.html')
            else:
                return render(request, 'encryptedSecrets/partials/sent_failure.html')    


class SecretsShareSecret(View):
    def get(self,request, pk):
        try:
            sharedsecret = SharedSecret.objects.get(id=pk)
        except:
            return render(request, 'encryptedSecrets/notfound.html')
        accessed = sharedsecret.accessed
        msg = ''
        print(sharedsecret)
        if not request.user.is_authenticated:
            
            accessed += 1
            if sharedsecret.ttl - accessed <= 0:
                #sharedsecret.delete()
                SharedSecret.objects.filter(id=pk).delete()
                msg = 'The secret has been deleted'
                message = msg
            else:
                sharedsecret.accessed = accessed
                sharedsecret.save(update_fields=['accessed'])
                message = 'Accessed secret: ' +  str(sharedsecret.ttl - accessed) + ' clicks left.'
                name = sharedsecret.name

        print(sharedsecret)
        clicksLeft = sharedsecret.ttl - accessed
        context = {
            'secret': sharedsecret,
            'next': 'encryptedSecrets:secrets',
            'page': 'share',
            'msg': message,
            'clicksLeft': clicksLeft
        }
    
        return render(request, 'encryptedSecrets/view_secret.html', context)


def email_secret(email, url):
    
    html = """\
    Congratulations!  You've been sent a secret!  

    Please click the link below to view your secret.

    <a href=""" + url + """ >View Secret.</a>
           """
    response = email_user(email, html)

    if response['result'] == 0:
        return False
            
    return True

class SecretsViewSecrets(LoginRequiredMixin, View):
    def get(self, request):
        pk = request.user.id
        user = User.objects.get(id=pk)
        
        secrets = user.sharedsecret_set.all()

        context = {
            'secrets': secrets,
            'action': {
                    'name': 'Secret',
                    'view_url': 'secrets:secret_view',
                    'edit_url': 'secrets:secret_edit',
                    'delete_url': 'secrets:secret_delete',
                    'create_url': 'secrets:secret_add',
                    
                }
        }
        return render(request, 'encryptedSecrets/secrets_htmx.html', context)
        
class SecretsEditSecret(LoginRequiredMixin, View):
    def get(self, request, pk):
        sharedsecret = SharedSecret.objects.get(id=pk)
        context = {
            'secret': sharedsecret,
            'next': 'secrets:secrets',
            'page': 'edit'
        }
        return render(request, 'encryptedSecrets/view_secret.html', context)

    def post(self, request, pk):
        sharedsecret = SharedSecret.objects.get(id=pk)
        sharedsecret.text = request.POST.get('secret')
        sharedsecret.ttl = request.POST.get('ttl')
        sharedsecret.save()
        return redirect('secrets:secrets')

class SecretsDeleteSecret(LoginRequiredMixin, View):
    def delete(self, request, pk):
        sharedsecret = SharedSecret.objects.get(id=pk)
        sharedsecret.delete()

        id = request.user.id
        user = User.objects.get(id=id)
        
        secrets = user.sharedsecret_set.all()
        context = {
            'secrets': secrets,
            'action': {
                    'name': 'Secret',
                    'view_url': 'secrets:secret_view',
                    'edit_url': 'secrets:secret_edit',
                    'delete_url': 'secrets:secret_delete',
                    'create_url': 'secrets:secret_add',
                    
                }
        }
        #return redirect('secrets:secrets')
        return render(request, 'encryptedSecrets/partials/secretlist.html', context)
