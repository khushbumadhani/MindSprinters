
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.SET_NULL , null=True)
    # email_address=models.CharField(max_length=55,unique=True,null=True)
    bio=models.TextField(blank=True,null=True)
    profile_img=models.ImageField(upload_to='profile_images',default='user.png',blank=True,null=True)
    location=models.CharField(max_length=100,blank=True,null=True)
    GENDER=(
        ('MALE','MALE'),
        ('FEMALE','FEMALE'),
        ('OTHER','OTHER')
    )
    gender=models.CharField(max_length=6,choices=GENDER,blank=True,null=True)

    def __str__(self):
        return f"{self.user}"
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"



