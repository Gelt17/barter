from django import forms
from .models import Ad, ExchangeProposal


class AdCreateForm(forms.ModelForm):
    """
    Форма добавления статей на сайте
    """

    class Meta:
        model = Ad
        fields = ('title', 'category', 'description', 'image_url', 'condition')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

class AdUpdateForm(AdCreateForm):
    """
    Форма обновления статьи на сайте
    """

    class Meta:
        model = Ad
        fields = AdCreateForm.Meta.fields

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        
class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_receiver', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'ad_receiver': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        exclude_ad = kwargs.pop('exclude_ad', None)
        super().__init__(*args, **kwargs)
        
        if user:
            queryset = Ad.objects.exclude(user=user)
            if exclude_ad:
                queryset = queryset.exclude(id=exclude_ad)
            self.fields['ad_receiver'].queryset = queryset