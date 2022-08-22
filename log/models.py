from django.db import models
from datetime import datetime
from django.conf import settings
from django.db import connections


#db = settings.DB

# Create your models here.
class Log(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    ip = models.CharField(max_length=20, null=False, blank=False)
    message = models.CharField(max_length=150, null=False, blank=False)
    owner = models.IntegerField(null=False, blank=False)
    created = models.CharField(max_length=200,null=True, blank = True)
    #created = models.DateTimeField()
    
    

    def save_log(self):
 
       
        with connections['logs'].cursor() as cursor:
            self.now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            print(self.now)
            print(type(self.now))
            response = cursor.execute("INSERT INTO log_log (NAME, IP, MESSAGE, OWNER, CREATED) VALUES (%s, %s, %s, %s, %s)", [self.name, str(self.ip), self.message, self.owner,self.now])
            cursor.close()
            print(response)
            
        return response

    

    '''
    def __init__(self, secret_name, ip, message, owner):
        self.secret_name = secret_name
        self.ip = ip
        self.message = message
        self.owner = owner
        self.datetimestamp = datetime.timestamp(datetime.now())
    '''

    
            
        
    