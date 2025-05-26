from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
class Ad(models.Model):
    
    """
    Модель объявлений
    """
    
    STATUS_OPTIONS = (
        ('new', 'Новое'),
        ('used', 'б/у')
    )
    
    user = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT, related_name='author_ad', default=1)
    title = models.CharField(verbose_name='Название записи', max_length=255)
    description = models.TextField(verbose_name='Краткое описание', max_length=500)
    image_url = models.ImageField(default='default.jpg', verbose_name='Изображение товара', blank=True, upload_to='images/ad/%Y/%m/%d/',
    validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))])
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='ads', verbose_name='Категория')
    condition = models.CharField(choices=STATUS_OPTIONS,verbose_name='Состояние товара', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    
    class Meta:
        db_table = 'ads_ad'
        ordering = ['-created_at']
        verbose_name = 'Реклама'
        verbose_name_plural = 'Рекламы'

    def __str__(self):
        return self.title

class Category(MPTTModel):
    """
    Модель категорий с вложенностью
    """
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='Описание категории', max_length=300)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('title',)

    class Meta:
        """
        Название модели в админ панели, таблица с данными
        """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'

    def __str__(self):
        """
        Возвращение заголовка категории
        """
        return self.title

class ExchangeProposal(models.Model):
        
        STATUS_EXCHANGE = (
        ('awaiting', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена')
        )
        
        ad_sender = models.ForeignKey(to=Ad, verbose_name='Отправитель', on_delete=models.SET_DEFAULT, related_name='sent_proposals', default=1)
        ad_receiver = models.ForeignKey(to=Ad, verbose_name='Отправитель', on_delete=models.SET_DEFAULT, related_name='received_proposals', default=1)
        comment = models.TextField(verbose_name='Комментарий', max_length=500)
        status = models.CharField(choices=STATUS_EXCHANGE,verbose_name='Статус предложения', max_length=10)
        created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
        
        class Meta:
            ordering = ['-created_at']
            verbose_name = 'Предложение'
            verbose_name_plural = 'Предложения'
            db_table = 'exchange_proposal'
            
        def __str__(self):
            return self.title