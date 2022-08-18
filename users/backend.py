from django.contrib.auth.backends import BaseBackend

from .models import User
from tenant.models import TenantMembership
from tenant.utils import tenant_from_request

class check_tenant(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            print(user)
        except User.DoesNotExist:
            
            return None

        try:
            tenant = tenant_from_request(request)
            print(tenant)
            user_tenant = user.tenant.get(id=tenant.id)
            print(user_tenant)
        except:
            return None

        if user_tenant is None:
            return None
        return user