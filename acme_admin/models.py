from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser,Group
from django.contrib.auth import get_user_model

# Create your models here.


class AbstractDateTime(models.Model):

    '''
      this is an abstract model class created for abstracting it into every models containing two fields 
        - created_at
        - updated_at 
        - created_by
    '''

    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now_add=True)
    created_by       = models.ForeignKey('acme_admin.CustomUser',on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
            abstract = True



class CustomUser(AbstractUser,AbstractDateTime):

    '''
      Here i am using same class for users and admin by just adding,

       -  is_user
      and abstracted 2 Classes,

       - AbstractUser
       - AbstractDAteTime
    '''
    email        = models.CharField(max_length=256)
    is_user      = models.BooleanField(default=False)
    phone        = models.CharField(max_length=20,help_text = "Provide Phone number or Email address")
    user_department   = models.ForeignKey('acme_admin.Department',related_name='user_department',on_delete=models.CASCADE,help_text = "Assign Department for Users",blank=True,null=True)
    user_roles = models.ForeignKey(Group,on_delete=models.PROTECT,help_text = "Assign roles for users",blank=True,null=True)

    class Meta:
        ordering = ("username",)

class Department(AbstractDateTime):
    name = models.CharField(max_length=256)
    description = models.TextField()

Group.add_to_class(
    'is_active', models.BooleanField(default=True),
)


class Tickets(AbstractDateTime):
    priority = (
        ('first','First'),
        ('second','Second'),
    )

    ticket_id = models.CharField(max_length=100)
    subject = models.TextField()
    priority = models.CharField(max_length=100,choices=priority)