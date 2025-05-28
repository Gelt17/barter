from django.urls import path
from .views import AdListView, AdDetailView, AdCreateForm, AdCreateView, AdUpdateView, AdFromCategory, CreateExchangeView, UpdateExchangeView, ExchangeListView, AdDeleteView


urlpatterns = [
    path('', AdListView.as_view(), name='home'),
    path('ad/create/', AdCreateView.as_view(), name='ad_create'),
    path('ad/<slug:slug>/', AdDetailView.as_view(), name='ad_detail'),
    path('category/<slug:slug>/', AdFromCategory.as_view(), name="ad_by_category"),
    path('ad/<slug:slug>/update/', AdUpdateView.as_view(), name='ad_update'),
    path('ad/<int:ad_id>/exchange/', CreateExchangeView.as_view(), name='create_exchange'),
    path('exchange/<int:pk>/update/', UpdateExchangeView.as_view(), name='update_exchange'),
    path('exchange/list/', ExchangeListView.as_view(), name='exchange_list'),
    path('ad/<slug:slug>/delete/', AdDeleteView.as_view(), name='ad_delete'),
]