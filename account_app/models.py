from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django_jalali.db import models as jmodels


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError("Users must have an email address")

        user = self.model(
            phone=phone,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone = models.CharField(max_length=11, unique=True, verbose_name="تلفن همراه")
    email = models.EmailField(unique=True, verbose_name="ایمیل")
    fullname = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    national_code = models.CharField(max_length=11, verbose_name='کد ملی')
    birthdate = jmodels.jDateField(verbose_name='تاریخ تولد', null=True, blank=True)
    prize_amount = models.PositiveIntegerField(default=0, blank=True, verbose_name='مقدار جایزه')
    year = models.IntegerField(default=0, verbose_name='سال', editable=False)
    month = models.IntegerField(default=0, verbose_name='ماه', editable=False)
    day = models.IntegerField(default=0, verbose_name='روز', editable=False)
    hour = models.IntegerField(default=0, verbose_name='ساعت', editable=False)
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="زمان عضویت")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")
    is_active = models.BooleanField(default=False, verbose_name="وضعیت کاربر")
    is_admin = models.BooleanField(default=False, verbose_name="ادمین")

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربرها"

    def __str__(self):
        return self.fullname

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
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Otp(models.Model):
    token = models.CharField(max_length=100)
    phone = models.CharField(max_length=11, verbose_name='تلفن همراه')
    code = models.SmallIntegerField(verbose_name='کد اعتبار سنجی')
    expiration_date = jmodels.jDateTimeField(verbose_name='تاریخ انقضا')

    class Meta:
        verbose_name = 'اعتبار سنجی'
        verbose_name_plural = 'اعتبار سنجی ها'

    def __str__(self):
        return self.phone


class Ban(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'مسدود'
        verbose_name_plural = 'مسدود ها'

    def __str__(self):
        return str(self.user.phone)
