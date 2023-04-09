from django.shortcuts import render, redirect
from django.views import View

# Create your views here.


class Index(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'core/index.html')
        else:
            return redirect('encryptedSecrets:secret_add')

    
    
