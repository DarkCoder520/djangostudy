from django.db import models

# Create your models here.

#User表
class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64,null=False)
    def __str__(self):
        return "<{}-{}>".format(self.id,self.name)


#Book表
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64,null=False)