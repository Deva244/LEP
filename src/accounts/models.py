from django.db import models
from django.contrib.auth.models import ( AbstractBaseUser, BaseUserManager )
from PIL import Image

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    image        = models.ImageField(default='default.jpg', upload_to='profile_pics')
    email        = models.EmailField(max_length=255,unique=True)
    first_name   = models.CharField(max_length=30)
    last_name    = models.CharField(max_length=30)
    account_types = [
    ('student', 'Student'),
    ('teacher', 'Teacher'),
    ('manager', 'Manager') ]
    account_type = models.CharField(choices=account_types, max_length=7)
    active       = models.BooleanField(default=True)
    staff        = models.BooleanField(default=False)
    admin        = models.BooleanField(default=False)
    no_of_groups = models.IntegerField(default=0)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []
 
    def get_full_name(self): 
        full_name = self.first_name + ' ' + self.last_name
        return full_name

    def get_email(self):
        return self.email

    def get_account_type(self):
        return self.account_type

    def __str__(self):
        return self.email

    def get_no_of_groups(self):
        return self.no_of_groups

    # def save(self):
    #     super().save()
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    objects = UserManager()

