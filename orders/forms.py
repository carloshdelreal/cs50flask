from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ( AuthenticationForm, UserCreationForm )
from orders.models import Item, Extras, SellingArticle, Order, ItemGroup

class LoginForm (AuthenticationForm):
    class Meta:
        model = User
        fields = [ 'username', 'password']

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2"
        ]
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user
    
class SellingArticleForm(forms.ModelForm):
    # itemGroup = ItemGroup.objects.get(pk=3)
    # item = forms.ModelChoiceField(queryset=Item.objects.filter(itemGroup__exact=itemGroup.id))
    # extras = forms.ModelMultipleChoiceField(queryset=Extras.objects.filter(itemGroup__exact=1))
    # itemGroup = forms.ModelChoiceField(queryset=ItemGroup.objects.filter(id__exact=itemGroup.pk))
    class Meta:
        model = SellingArticle
        fields = ['item','quantity']
    
    def __init__(self, itemGroup, *args,**kwargs):
        super (SellingArticleForm, self).__init__(*args,**kwargs)
        self.fields['item'].queryset = Item.objects.filter(itemGroup__exact=itemGroup.id)
        
    def save(self, request, commit=True):
        SellingArticle = super(SellingArticleForm, self).save(commit=False)
        order = Order()
        order.user = request.user
        order.save()
        SellingArticle.sell_order = order
        SellingArticle.item = self.cleaned_data["item"]
        SellingArticle.quantity = self.cleaned_data['quantity']
        if commit:
            # for i in self.cleaned_data['extras']:
            #     eq = ExtraQuantity()
            #     eq.quantity = 1
            #     eq.extra = i
            #     eq.selling = SellingArticle
            #     eq.save()
            SellingArticle.save()
            
        return SellingArticle

class MenuSelectedForm(forms.Form):
    orderString = forms.CharField()