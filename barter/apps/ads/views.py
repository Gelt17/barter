from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Ad, Category, ExchangeProposal
from .forms import AdCreateForm, AdUpdateForm, ExchangeProposalForm
from .mixins import AuthorRequiredMixin
from django.urls import reverse_lazy
from django.db import models
from django.shortcuts import render
from django.db.models import Q

class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 2
    
    def get_queryset(self):
        queryset = super().get_queryset()

        category_slug = self.request.GET.get('category')
        conditions = self.request.GET.getlist('condition')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if conditions:
            queryset = queryset.filter(condition__in=conditions)

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['condition_options'] = [
        ('new', 'Новое'),
        ('used', 'Б/у'),
        ]
        context['selected_conditions'] = self.request.GET.getlist('condition')
        return context

class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context

class AdCreateView(LoginRequiredMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = Ad
    template_name = 'ads/ad_create.html'
    form_class = AdCreateForm
    login_url = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление рекламы'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class AdUpdateView(AuthorRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления материала на сайте
    """
    model = Ad
    template_name = 'ads/ad_update.html'
    context_object_name = 'ad'
    form_class = AdUpdateForm
    login_url = 'home'
    success_message = 'Запись была успешно обновлена!'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление рекламы: {self.object.title}'
        return context

    def form_valid(self, form):
        # form.instance.updater = self.request.user
        return super().form_valid(form)

class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user
    
    
class AdFromCategory(ListView):
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    category = None

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Ad.objects.filter(category__slug=self.category.slug)
        conditions = self.request.GET.getlist('condition')
        if not queryset:
            sub_cat = Category.objects.filter(parent=self.category)
            queryset = Ad.objects.filter(category__in=sub_cat)
            
        if conditions:
            queryset = queryset.filter(condition__in=conditions)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Записи из категории: {self.category.title}'
        context['condition_options'] = [
        ('new', 'Новое'),
        ('used', 'Б/у'),
        ]
        context['selected_conditions'] = self.request.GET.getlist('condition')
        return context

class CreateExchangeView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    template_name = 'exchange/create_proposal.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.ad_sender = Ad.objects.get(id=self.kwargs['ad_id'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('ad_detail', kwargs={'slug': self.object.ad_sender.slug})

class UpdateExchangeView(LoginRequiredMixin, UpdateView):
    model = ExchangeProposal
    fields = ['status']
    template_name = 'exchange/update_proposal.html'
    
    def get_queryset(self):
        return super().get_queryset().filter(ad_receiver__user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('ad_detail', kwargs={'slug': self.object.ad_receiver.slug})
    
class ExchangeListView(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    template_name = 'exchange/proposal_list.html'
    
    def get_queryset(self):
        status = self.request.GET.get('status')
        queryset = ExchangeProposal.objects.filter(
            models.Q(ad_sender__user=self.request.user) |
            models.Q(ad_receiver__user=self.request.user)
        )
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by('-created_at')

def ad_search(request):
    query = request.GET.get('q', '')
    results = []
    context = {
            'query': query,
            'ads': results,
        }
    
    if query:
        results = Ad.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        
        context['ads'] = results
        
    return render(request, 'ads/search.html', context)

def condition_view(request):
    condition_options = [
        ('new', 'Новое'),
        ('used', 'Б/у'),
    ]
    context = {
        'condition_options': condition_options,
    }
    return render(request, 'your_template.html', context)