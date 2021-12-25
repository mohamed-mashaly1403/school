from django.db import models

# Create your models here.
#overwrite django user model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser ,BaseUserManager
class account_manger(BaseUserManager):
    def create_user(self,first_name,last_name,email,username,password=None):
        if not email:
            raise ValueError('add your email')
        if not username:
            raise ValueError('add username')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password = password
        )
        user.is_admin = True
        user.is_superadmin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
class account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    username = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    user_img = models.ImageField(upload_to="img/users", blank=True)
    #required
    joined_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_superadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','username','last_name']
    objects = account_manger()
    def __str__(self):
        return self.email
    #must mention in overwrite
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,add_label):
        return True

    @property
    def image_url(self):
        if self.user_img and hasattr(self.user_img, 'url'):
            return self.user_img.url
class UserProfile(models.Model):
    user = models.OneToOneField(account,on_delete=models.CASCADE)
    city = models.CharField(max_length=20,blank=True)
    country = models.CharField(max_length=20,blank=True)
    def __str__(self):
        return self.user.first_name
