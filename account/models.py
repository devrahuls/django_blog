from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


#2ND STEP
#THIS IS REQUIRED, WE ALSO HAVE TO CREATE THE USER MANAGER
#Use BaseUserManager, if you have some extra fields apart from the some django defaults, otherwise use only UserManager
class MyAccountManager(BaseUserManager):
    #To create a user
    def create_user(self, email, username, password=None): #Fields that are required to create the custom user, will go into this parameter.
        if not email:
            raise ValueError("User must required an email")
        if not username:
            raise ValueError("User must required a username")

        user = self.model(
            email=self.normalize_email(email), #normalize_email()-> Converts all the letters into lowercase of an email. Its a method inside the BaseUserManager class.
            username=username
        )

        user.set_password(password) #Django Built in user methods provides these functionalities.
        user.save(using=self._db)
        return user
    
    #To create a super user
    def create_superuser(self, email, username, password):
            user = self.create_user(
            email=self.normalize_email(email), #normalize_email()-> Converts all the letters into lowercase of an email. Its a method inside the BaseUserManager class.
            password=password,
            username=username
            )
            user.is_admin = True
            user.is_staff = True
            user.is_superuser = True
            user.save(using=self._db)
            return user




#1ST STEP
# Create your models here.
class Account(AbstractBaseUser):
    email                       = models.EmailField(verbose_name="email" ,max_length=60, unique=True)
    username                    = models.CharField(max_length=30, unique=True)
    date_joined                 = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login                  = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                    = models.BooleanField(default=False)
    is_active                   = models.BooleanField(default=True)
    is_staff                    = models.BooleanField(default=False)
    is_superuser                = models.BooleanField(default=False)


    #WE CAN'T CHANGE THE USERNAME_FIELD & REQUIRED_FIELDS, BECAUSE THEY'RE PRE-DEFINED KEYWORDS.
    #Basically means, whatever you'll required when you login will put here, like email or username 
    USERNAME_FIELD = 'email'
    #Fields that are required during registration
    REQUIRED_FIELDS = ['username',]

    #3RD STEP
    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    #This is required when you wanna create your own custom user model
    def has_perm(self, perm, obj=None):
        return self.is_admin #Means, whoever the admin is, can edit the changes in the Database
    def has_module_perms(self, app_level):
        return True