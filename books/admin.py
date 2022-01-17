from django.contrib import admin

# Register your models here.
from .models import Library, Author, LiteratureCategory, Book
from .models import LoanedBook as Loaned


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    search_fields = ('library_name', 'address')
    list_display = ('library_name', 'address', 'description')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields  = ('full_name',)
    list_display = ('full_name', 'date_birth', 'date_death')
    empty_value_display = 'not dead'


@admin.register(LiteratureCategory)
class LiteratureCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name','kutubxonadagi_kitoblar_soni', 'kitobxonlar_foydalanayotgan_kitoblar_soni')
    
    def kutubxonadagi_kitoblar_soni(self, obj):
        return obj.book_set.all().count()

    def kitobxonlar_foydalanayotgan_kitoblar_soni(self, obj):
        smth = Loaned.objects.filter(loan_status='Hali qaytarilmadi!',book__literature_category_id=obj )
        return smth.count()

   


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ('isbn','book_title', 'author__full_name' )
    list_display = ('isbn', 'book_title', 'kitob_mualliflari','kitob_janri', 'published_year' )
    autocomplete_fields = ('author', 'literature_category_id')

    def kitob_mualliflari(self,obj):
        return "\n".join([p.full_name for p in obj.author.all()])

    def kitob_janri(self,obj):
        return "\n".join([p.name for p in obj.literature_category_id.all()])    

def kitobni_kech_qaytardi(modeladmin, request, queryset):
    queryset.update(loan_status='Kechiktirib qaytarildi')

def kitobni_vaqtida_qaytardi(modeladmin, request, queryset):
    queryset.update(loan_status='Vaqtida qaytarildi!')

def kitobni_qaytarmadi(modeladmin, request, queryset):
    queryset.update(loan_status='Hali qaytarilmadi!')


@admin.register(Loaned)    
class LoanedBook(admin.ModelAdmin):
    search_fields = ('member__email', 'member__passport_id', 'member__first_name', 'member__last_name', 'book__isbn', 'book__book_title', 'book__author__full_name')
    list_display = ('kitobning_nomi', 'kitobxonning_ismi_familiyasi','date_loaned', 'date_due','loan_status', 'muddat_tugadimi', 'kun_qaytarmadi' )
    list_filter  = ('loan_status',)
    autocomplete_fields = ('member', 'book')
    actions = (kitobni_kech_qaytardi, kitobni_vaqtida_qaytardi, kitobni_qaytarmadi)
    
    def kitobxonning_ismi_familiyasi(self,obj):
        return "%s %s"%(obj.member.first_name, obj.member.last_name) 

    def kitobning_nomi(self,obj):
        return obj.book.book_title 
