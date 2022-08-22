
from django.conf import settings
from datetime import datetime
from django.db import connections

from .models import Log

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def read_logs(pk):
    with connections['logs'].cursor() as cursor:
      
        cursor.execute("SELECT ID, NAME, IP, MESSAGE, CREATED FROM log_log WHERE OWNER = %s", [pk])
       
        rows = dictfetchall(cursor)

        cursor.close()
    return rows

def dictfetchall(cursor):
    
    columns = [col[0].replace(')','').split('.')[2] for col in cursor.description]
   
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]