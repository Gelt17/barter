from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models  import Ad, Category, ExchangeProposal

# Create your tests here.

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Ad, Category, ExchangeProposal

class AdTests(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(title='Техника', slug='tehnika')
        
        self.ad = Ad.objects.create(
            user=self.user,
            title='Пример объявления',
            description='Описание объявления',
            category=self.category,
            condition='new'
        )
        self.client = Client()

    def test_create_ad(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('ad_create')
        data = {
            'title': 'Новое объявление',
            'description': 'Описание нового объявления',
            'category': self.category.id,
            'condition': 'used',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ad.objects.filter(title='Новое объявление').exists())

    def test_edit_ad(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('ad_update', kwargs={'slug': self.ad.slug})
        data = {
            'title': 'Обновленное объявление',
            'description': 'Обновленное описание',
            'category': self.category.id,
            'condition': 'used',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Обновленное объявление')


    def test_search_ads(self):
    # Явно создаем объявление с уникальным названием
        search_ad = Ad.objects.create(
        user=self.user,
        title='Уникальное тестовое объявление',
        description='Описание для поиска',
        category=self.category,
        condition='new'
        )
    
    # Ищем по части названия в нижнем регистре
        url = reverse('ad_search') + '?q=Уникальное'
        response = self.client.get(url)
    
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Уникальное тестовое объявление')

    def test_create_exchange_proposal(self):
    # Создаем второго пользователя и его объявление (получателя)
        receiver_user = User.objects.create_user(username='receiver', password='testpass')
        receiver_ad = Ad.objects.create(
            user=receiver_user,
            title='Объявление получателя',
            description='Описание',
            category=self.category,
            condition='new'
        )
    
        self.client.login(username='testuser', password='testpass')
        url = reverse('create_exchange', kwargs={'ad_id': self.ad.pk})
        data = {
            'ad_receiver': receiver_ad.id,  # обязательное поле
            'comment': 'Предлагаю обмен',   # обязательное поле
        }
        response = self.client.post(url, data)
    
        # После успешного создания должно быть перенаправление (302)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ExchangeProposal.objects.filter(ad_sender=self.ad, ad_receiver=receiver_ad).exists())
        
    
    def test_delete_ad(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('ad_delete', kwargs={'slug': self.ad.slug})  
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ad.objects.filter(slug=self.ad.slug).exists())