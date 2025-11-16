from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator, MaxLengthValidator

# ==============================================================================
# TASK 0: CUSTOM USER MODEL
# ==============================================================================

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    profile_photo = models.ImageField(_('profile photo'), upload_to='profile_photos/', null=True, blank=True)
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

# ==============================================================================
# TASK 1: BOOK MODEL WITH PERMISSIONS
# ==============================================================================

class Book(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(2), MaxLengthValidator(200)])
    author = models.CharField(max_length=100, validators=[MinLengthValidator(2), MaxLengthValidator(100)])
    description = models.TextField(max_length=1000, validators=[MaxLengthValidator(1000)], blank=True)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, validators=[MinLengthValidator(10)], unique=True)
    created_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        # TASK 1: Custom permissions
        permissions = [
            ("can_view", "Can view books"),
            ("can_create", "Can create books"), 
            ("can_edit", "Can edit books"),
            ("can_delete", "Can delete books"),
            ("can_manage_books", "Can create, update, and delete books"),
        ]

    def __str__(self):
        return f"{self.title} by {self.author}"
