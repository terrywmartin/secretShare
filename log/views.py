from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models.functions import Lower


from users.models import User
from .models import Log
from .utils import read_logs

# Create your views here.
class LogsViewLogs(LoginRequiredMixin, View):
    def get(self, request):
        order_by_param = request.GET.get('order_by','name')
        sort_order = request.GET.get('sort', 'asc')
        pk = request.user.id
        logs = Log.objects.using('logs').filter(owner = pk)
        """  if order_by_param == 'name':
            if sort_order == 'asc':
                logs = Log.objects.using('logs').filter(owner = pk).order_by('name')
            else:
                logs = Log.objects.using('logs').filter(owner = pk).order_by(Lower('name').desc())
        else:
            if sort_order == 'asc':
                logs = Log.objects.using('logs').filter(owner = pk).order_by('created')
            else:
                logs = Log.objects.using('logs').filter(owner = pk).order_by(Lower('created').desc())
        """

        print(logs)
        #logs = read_logs(pk=pk)
        
        paginator = Paginator(logs, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'order_by': order_by_param,
            'sort': sort_order
        }
        return render(request, 'log/view_logs.html', context)

class LogsSearchLogs(LoginRequiredMixin, View):
    def post(self, request):
        pass
      