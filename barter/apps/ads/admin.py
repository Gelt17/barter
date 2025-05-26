from django.contrib import admin
from .models import Ad, Category, ExchangeProposal
from django_mptt_admin.admin import DjangoMpttAdmin
# Register your models here.

@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    """
    Админ-панель модели категорий
    """
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Ad)
admin.site.register(ExchangeProposal)