from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from apps.accounts.utils import unique_slugify
from django.utils import timezone

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
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True)
    description = models.TextField(verbose_name='Краткое описание', max_length=500)
    image_url = models.ImageField(default='default.jpg', verbose_name='Изображение товара', blank=True, upload_to='images/ad/%Y/%m/%d/',
    validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))])
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='ads', verbose_name='Категория')
    condition = models.CharField(choices=STATUS_OPTIONS,verbose_name='Состояние товара', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    updated_at = models.ForeignKey(to=User, verbose_name='Обновил', on_delete=models.SET_NULL, null=True, related_name='updater_ads', blank=True)
    
    class Meta:
        db_table = 'ads_ad'
        ordering = ['-created_at']
        verbose_name = 'Реклама'
        verbose_name_plural = 'Рекламы'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """
        Получаем прямую ссылку на статью
        """
        return reverse('ad_detail', kwargs={'slug': self.slug}) 
    
    def save(self, *args, **kwargs):
        """
        При сохранении генерируем слаг и проверяем на уникальность
        """
        self.slug = unique_slugify(self, self.title, self.slug)
        super().save(*args, **kwargs)

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

    def get_absolute_url(self):
        """
        Получаем прямую ссылку на категорию
        """
        return reverse('ad_by_category', kwargs={'slug': self.slug})

    def __str__(self):
        """
        Возвращение заголовка статьи
        """
        return self.title

class ExchangeProposal(models.Model):
        
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]
        
    ad_sender = models.ForeignKey('Ad', on_delete=models.CASCADE, related_name='sent_proposals', verbose_name='Объявление отправителя')
    ad_receiver = models.ForeignKey('Ad', on_delete=models.CASCADE, related_name='received_proposals', verbose_name='Объявление получателя')
    comment = models.TextField('Комментарий', max_length=500)
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Предложение обмена'
        verbose_name_plural = 'Предложения обмена'
        constraints = [models.UniqueConstraint(fields=['ad_sender', 'ad_receiver'], name='unique_proposal')]

    def __str__(self):
        return f"Предложение #{self.id} ({self.get_status_display()})"