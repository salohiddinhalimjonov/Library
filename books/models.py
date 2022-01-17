from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
import os
from datetime import date
from django.conf import settings
from django.utils import timezone
from members.models import User

def book_image_path(instance, filename):
    file_format = str(filename).split('.')[-1]
    filename = f"{uuid4()}.{file_format}"
    return os.path.join("thumb/", filename)

def book_video_path(instance,filename):
    file_format = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{file_format}"
    return os.path.join("product/video", filename)


class Library(models.Model):

    library_name = models.CharField(_("Kutubxina numi:"), max_length=128)
    address = models.CharField(_("Kutubxona manzili:"), max_length=255)
    photo = models.ImageField(_("Rasmi:"), upload_to=book_image_path, null=True,blank=True)
    video = models.FileField(_("Videosi:"), upload_to=book_video_path, null=True,blank=True)
    description = models.TextField(_("Kutubhona haqida batafsil:"), null=True, blank=True)
    
    class Meta:
        verbose_name = _("Kutubxona:")
        verbose_name_plural = _("Kutubxonalar:")

    def __str__(self):
        return self.library_name    

class Author(models.Model):

    full_name = models.CharField(_("Yozuvchining ismi va familiyasi:"), max_length=128,default='Not known')
    date_birth = models.DateField(_("Yozuvchining tug\'ilgan sanasi:"))
    date_death = models.DateField(_("Yozuvchining vafot etgan sanasi:"), null=True, blank=True)

    class Meta:
        verbose_name = _("Kitob muallifi:")
        verbose_name_plural = _("Kitob mualliflari:")
       

    def __str__(self):
        return self.full_name 


class LiteratureCategory(models.Model):
    
    name = models.CharField(_("Asar janri:"),max_length=128)
    
    class Meta:
        verbose_name = _("Asar janri:")
        verbose_name_plural = _("Asar janrlari")

    def __str__(self):
        return self.name    


class Book(models.Model):

    isbn = models.CharField(_("Kitob raqami:"), unique=True, max_length=13)
    book_title =  models.CharField(_("Kitobning nomi:"), max_length=128)
    author = models.ManyToManyField(Author, verbose_name = _('Kitob muallifi:'))
    literature_category_id = models.ManyToManyField(LiteratureCategory,verbose_name=_("Adabiy janrlar:"))
    published_year = models.DateField(_("Kitob nashr qilingan sana:"))
    
    class Meta:
        verbose_name = _("Kitob:")
        verbose_name_plural = _("Kitoblar")
    
    def __str__(self):
        return self.book_title


class LoanedBook(models.Model):

    CHOICES = (('Vaqtida qaytarildi!', 'Vaqtida qaytarildi!'),
                ('Kechiktirib qaytarildi', 'Kechiktirib qaytarildi'),
                ('Hali qaytarilmadi!', 'Hali qaytarilmadi!'))

    book = models.ForeignKey(Book, on_delete = models.CASCADE, verbose_name = _("Kitob nomi:"))
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, verbose_name = _("Kitob oluvchi:"))
    date_loaned = models.DateField(_("Kitob olingan sana:"))
    date_due = models.DateField(_("Kitob qaytarilishi kerak bo\'lgan sana:"))
    date_returned = models.DateField(_("Kitob qaytarilgan sana:"), null=True, blank=True)
    loan_status = models.TextField(_('Kitob qaytarildimi:'),choices=CHOICES, default='Hali qaytarilmadi!' )
   
    def muddat_tugadimi(self):
        if self.date_due and date.today() > self.date_due and self.loan_status=='Hali qaytarilmadi!':
            return "Ha"
        elif self.date_due and date.today()> self.date_due and self.loan_status == "Kechiktirib qaytarildi" or self.loan_status=='Vaqtida qaytarildi!':
            return '----'    
        else:
            return "Yo\'q"

    def kun_qaytarmadi(self):
        a = date.today()
        b = self.date_due
        if a>b and self.loan_status=='Hali qaytarilmadi!':
            return date.today() - self.date_due
            

        elif self.loan_status == "Kechiktirib qaytarildi":
            return self.date_returned - self.date_due
            
        else:
            return '----'     


    class Meta:
        verbose_name = _("Ijaraga olingan kitob:")
        verbose_name_plural = _("Ijaraga olingan kitoblar:")
        

    def __str__(self):
        return self.book.book_title