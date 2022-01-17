from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.validators import RegexValidator
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    email = models.CharField(_("Email:"),unique=True, max_length=128)
    first_name = models.CharField(_("Ism:"), max_length=128)
    last_name = models.CharField(_("Familiya:"), max_length = 128)
    passport_id = models.CharField(("Passport raqam:"), max_length = 20)
    phone_number = models.CharField(("Telefon raqam:"), max_length = 12,
    validators=[RegexValidator(regex=r'^(\+?998)?([. \-])?((\d){2})([. \-])?(\d){3}([. \-])?(\d){2}([. \-])?(\d){2}$',
                                                        message="Given phone number is not valid")])
    address = models.CharField(("Manzil:"), max_length = 128)
    date_joined = models.DateTimeField(_("Ro\'yhatdan o\'tgan sanasi:"), default=timezone.now)

    is_superuser = models.BooleanField(_("Administratormi?"), default=False, 
    help_text = _("Administratorlik huquqi"))

    is_staff = models.BooleanField(_("Moderatormi"),default=False,
    help_text = _("Admin qismiga kirish huquqi"))    

    is_active = models.BooleanField(_("Aktivmi?"),default=True,
    help_text = _("Saytga kirish huquqi"))
    
    objects = UserManager()
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("Kutubxona a\'zosi")
        verbose_name_plural = _("Kutubxona a\'zolari")
       
        
    def __str__(self):
        return "%s %s"%(self.first_name, self.last_name)