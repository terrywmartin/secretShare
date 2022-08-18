from distutils.log import Log
from multiprocessing import sharedctypes
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .forms import SharedSecretForm
from .models import SharedSecret
from users.utils import email_user
from users.models import User

# Create your views here.
class SecretsAddSecret(LoginRequiredMixin,View):
    def get(self, request):
        form = SharedSecretForm()
        profile = request.user.userprofile
        settings = profile.usersetting
        context = {
            'secret': '',
            'next': 'secrets:secrets',
            'form': form,
            'settings': settings
        }
       
        return render(request, 'encryptedSecrets/add_secret.html', context)
    def post(self, request):
        
        plain_secret = request.POST.get('secret')
        name = request.POST.get('name')
        ttl = request.POST.get('ttl')
        sharedsecret = SharedSecret(name=name,text=plain_secret,ttl=ttl)
        sharedsecret.owner = request.user
        sharedsecret.save()
        return redirect('secrets:secrets')

class SecretsViewSecret(View):
    def get(self,request, pk):
        try:
            sharedsecret = SharedSecret.objects.get(id=pk)
        except:
            return render(request, 'encryptedSecrets/notfound.html')
        accessed = sharedsecret.accessed
        msg = ''
    
        if not request.user.is_authenticated:
            accessed += 1
            if sharedsecret.ttl - accessed <= 0:
                sharedsecret.delete()
                msg = 'The secret has been deleted'
            else:
                sharedsecret.accessed = accessed
                sharedsecret.save(update_fields=['accessed'])
        
        if request.method == 'POST':
            
            if request.user.is_authenticated:
                email = request.POST.get('email')
                if email == "":
                    return render(request, 'encryptedSecrets/partials/sent_failure.html')    
                
                response = email_secret(email, request.build_absolute_uri())
                if response:
                    return render(request, 'encryptedSecrets/partials/sent_success.html')
                else:
                    return render(request, 'encryptedSecrets/partials/sent_failure.html')    

        clicksLeft = sharedsecret.ttl - accessed
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
